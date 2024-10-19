import ast
from langchain.agents import tool
import time
from pydantic import BaseModel, Field

class EvaluateResponseInput(BaseModel):
    query: str = Field(description="should be a user's response, correct answer, difficulty and taxonomy level in a string format")

@tool("evaluate_response", args_schema=EvaluateResponseInput, return_direct=True)
def evaluate_response(query: str) -> dict:
    """
    Evaluates the user's response and returns if the answer is correct or incorrect.

    Args:
        query: A string with the user's response, correct answer, difficulty and taxonomy level.

    Returns:
        dict: A result indicating whether the user's response is correct or incorrect, 
        along with metadata such as feedback, question difficulty, and taxonomy.
    """
    start_time = time.time()

    # Normalize and compare answers
    query_dict = ast.literal_eval(query)
    user_response = query_dict['user_response'].strip().lower()
    correct_answer = query_dict['correct_answer'].strip().lower()

    if user_response == correct_answer:
        result = {
            "correct": True,
            "feedback": "Correct answer!"
        }
    else:
        result = {
            "correct": False,
            "feedback": f"Incorrect. The correct answer is {correct_answer.capitalize()}."
        }

    end_time = time.time()
    execution_time = end_time - start_time
    result["execution_time"] = execution_time
    print(result["feedback"])
    print("Preparing for next question...\n")
    return result
