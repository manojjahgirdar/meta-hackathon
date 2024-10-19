from langchain.agents import tool
import time

@tool("evaluate_response")
def evaluate_response(user_response: str, correct_answer: str, difficulty: str, taxonomy: str) -> dict:
    """
    Evaluates the user's response and returns if the answer is correct or incorrect.

    Args:
        user_response: A string with the user's response.
        correct_answer: A string with the correct answer.
        difficulty: A string with the difficulty level.
        taxonomy: A string with the taxonomy level.

    Returns:
        dict: A result indicating whether the user's response is correct or incorrect, 
        along with metadata such as feedback, question difficulty, and taxonomy.
    """
    start_time = time.time()

    # Normalize and compare answers
    user_response = user_response.strip().lower()
    correct_answer = correct_answer.strip().lower()

    if user_response == correct_answer:
        result = {
            "correct": True,
            "feedback": "Correct answer!",
            "difficulty": difficulty,
            "taxonomy": taxonomy
        }
    else:
        result = {
            "correct": False,
            "feedback": f"Incorrect. The correct answer is {correct_answer}.",
            "difficulty": difficulty,
            "taxonomy": taxonomy
        }

    end_time = time.time()
    execution_time = end_time - start_time
    result["execution_time"] = execution_time
    
    return result
