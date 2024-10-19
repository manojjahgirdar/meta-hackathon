from flask import Flask, jsonify, render_template
from flask_socketio import SocketIO, emit
from threading import Thread

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    # This will serve the HTML page to the user
    return render_template('index.html')

# Handler for receiving the question from the backend
@socketio.on('ask_question')
def handle_ask_question(data):
    print(f"Question received from backend: {data}")
    # Emit the question to the frontend
    emit('ask_question', data, broadcast=True)

@socketio.on('final_summary')
def handle_final_summary(data):
    print(f"Final summary received from backend: {data}")
    # Emit the final summary to the frontend
    emit('final_summary', data, broadcast=True)
    
# Handler for receiving the answer from the frontend
@socketio.on('question_response')
def handle_question_response(response):
    # Add a log to see if this is getting called
    print(f"Response received from frontend: {response}")
    # Here you would process the response or pass it back to your LangChain tool
    emit('question_response', response, broadcast=True)

@app.route('/invoke_agent')
def invoke_agent():
    from main import agent_main
    # Run agent_main in a separate thread
    Thread(target=agent_main).start()
    # Immediately return "ok"
    return jsonify({"status": "Agent invoked"})
    

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
