import ast
import json
from langchain.agents import tool
import time
from pydantic import BaseModel, Field

class AskUserInput(BaseModel):
    question: str = Field(description="should be a question, options, taxonomy and difficulty")

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
    question_json = ast.literal_eval(question)
    # {"A": "To absorb water and minerals", "B": "To synthesise food from sunlight", "C": "To release oxygen", "D": "To absorb carbon dioxide"} convert to string format
    options = ast.literal_eval(question_json['options'])
    options_str = "\n".join([f"{option}: {option_desc}" for option, option_desc in options.items()])
    formatted_question = f"(Difficulty: {question_json['difficulty']}, Taxonomy: {question_json['taxonomy']}) Question: {question_json['question']}\nOptions:\n{options_str}"
    user_response = input(formatted_question+"\nAnswer: ")
    
    end_time = time.time()
    execution_time = end_time - start_time
    print(user_response)
    return user_response