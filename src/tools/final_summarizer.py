import ast
import time
from pydantic import BaseModel, Field
from langchain.agents import tool
import socketio

class FinalSummarizerInput(BaseModel):
    final_summary: str = Field(description="should be a final summary of the conversation")

# Create a Socket.IO client
sio = socketio.Client()

# Connect to the Socket.IO server
sio.connect('http://localhost:5000')  # Replace with your backend server's address

@tool("final_summarizer", args_schema=FinalSummarizerInput, return_direct=True)
def final_summarizer(final_summary: str) -> str:
    """
    Prompts the user with a question and returns the user's response.

    Args:
        final_summary: The final summary of the conversation.

    Returns:
        The user's response as a string.
    """
    start_time = time.time()

    # Prepare the question for frontend
    final_summary_json = ast.literal_eval(final_summary)
    # "{\"score\": 4, \"rank\": \"Excellent\", \"strengths\": [\"Understanding plant growth\", \"Analyzing plant relationships\"], \"weaknesses\": [\"Evaluating symbiotic relationships\"]}"
    formatted_question = {
        "score": final_summary_json["score"],
        "rank": final_summary_json["rank"],
        "strengths": final_summary_json["strengths"],
        "weaknesses": final_summary_json["weaknesses"]
    }

    # Send the question to the frontend
    sio.emit('final_summary', formatted_question)

    end_time = time.time()
    execution_time = end_time - start_time
    return f"Final summary sent to frontend in {execution_time:.2f} seconds"
