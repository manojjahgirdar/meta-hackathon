import ast
from langchain.agents import tool
import time
import json
from pydantic import BaseModel, Field
from src.core.db_crud import QuestionDB

class QuestionPickerInput(BaseModel):
    query: str = Field(description="should be a difficulty and taxonomy level")

@tool("question_picker", args_schema=QuestionPickerInput, return_direct=True)
def question_picker(query: str) -> dict:
    """
    Picks a question based on the difficulty and taxonomy.

    Args:
        query: A string with the difficulty and taxonomy level.
    
    Returns:
        dict: A dictionary with the following keys: question, correct_answer.
    """
    # convert the query to a dictionary
    query_dict = ast.literal_eval(query) # this will fail as the input is "{'difficulty': 'Easy', 'taxonomy': 'Remembering'}" 
    # so we need to convert it to a dictionary
    
    start_time = time.time()
    difficulty = query_dict['difficulty'].strip().capitalize()
    taxonomy = query_dict['taxonomy'].strip().capitalize()
    
    # use the db_crud to fetch a random question based on the difficulty and taxonomy
    question_db = QuestionDB()
    question = question_db.read_random(difficulty, taxonomy)
    question_db.close()

    # print(f"Question: {question[1]}, Answer: {question[2]}, Difficulty: {question[4]}, Taxonomy: {question[5]}, Options: {question[3]}")

    end_time = time.time()
    execution_time = end_time - start_time
    return {
        'question': question[1],
        'correct_answer': question[2],
        'options': question[3],
        'difficulty': question[4],
        'taxonomy': question[5]
    }
