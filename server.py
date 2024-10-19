from flask import Flask, render_template
from flask_socketio import SocketIO, emit

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

# Handler for receiving the answer from the frontend
@socketio.on('question_response')
def handle_question_response(response):
    # Add a log to see if this is getting called
    print(f"Response received from frontend: {response}")
    # Here you would process the response or pass it back to your LangChain tool
    emit('question_response', response, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)