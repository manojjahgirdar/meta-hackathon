import ast
import time
from pydantic import BaseModel, Field
from langchain.agents import tool
import socketio

class AskUserInput(BaseModel):
    question: str = Field(description="should be a question, options, taxonomy and difficulty")

# Create a Socket.IO client
sio = socketio.Client()

# Connect to the Socket.IO server
sio.connect('http://localhost:5000')  # Replace with your backend server's address

response_received = None

# Callback to receive the response from the frontend
@sio.on('question_response')
def receive_response(data):
    global response_received
    response_received = data
    print(f"Response received from frontend (in callback): {response_received}")

@tool("ask_user", args_schema=AskUserInput, return_direct=True)
def ask_user(question: str) -> str:
    """
    Prompts the user with a question and returns the user's response.

    Args:
        question: The question to ask the user.

    Returns:
        The user's response as a string.
    """
    start_time = time.time()

    # Prepare the question for frontend
    question_json = ast.literal_eval(question)
    options = ast.literal_eval(question_json['options'])
    options_str = "\n".join([f"{option}: {option_desc}" for option, option_desc in options.items()])
    formatted_question = {
        "difficulty": question_json["difficulty"],
        "taxonomy": question_json["taxonomy"],
        "question": question_json["question"],
        "options": options
    }

    # Send the question to the frontend
    sio.emit('ask_question', formatted_question)

    # Wait for the response
    global response_received
    response_received = None
    while response_received is None:
        time.sleep(0.1)  # Keep polling until a response is received

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Response received: {response_received}")
    return response_received
