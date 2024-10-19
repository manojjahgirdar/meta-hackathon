from langchain.agents import tool
import time

from src.core.db_crud import QuestionDB

@tool("question_picker")
def question_picker(difficulty: str, taxonomy: str) -> dict:
    """
    Picks a question based on the difficulty and taxonomy.

    Args:
        difficulty: A string with the difficulty level.
        taxonomy: A string with the taxonomy level.
    
    Returns:
        dict: A dictionary with the following keys: question, correct_answer.
    """
    start_time = time.time()
    difficulty = difficulty.strip().capitalize()
    taxonomy = taxonomy.strip().capitalize()
    
    # use the db_crud to fetch a random question based on the difficulty and taxonomy
    question_db = QuestionDB()
    question = question_db.read_random(difficulty, taxonomy)
    question_db.close()

    print(f"Question: {question[1]}, Answer: {question[2]}, Difficulty: {question[4]}, Taxonomy: {question[5]}, Options: {question[3]}")

    end_time = time.time()
    execution_time = end_time - start_time
    return {
        'question': question[1],
        'correct_answer': question[2],
        'options': question[3],
        'difficulty': question[4],
        'taxonomy': question[5]
    }
