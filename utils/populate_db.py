# I have a questions.json file in the db folder. I want to import the data from the json file into the database.
# here is a sample of the data in the json file:
# [
#       {
#         "question": "What is the importance of plant breeding in agriculture?",
#         "options": {
#             "A": "To increase crop yield",
#             "B": "To improve crop quality",
#             "C": "To reduce pesticide use",
#             "D": "To increase food security"
#         },
#         "answer": "D",
#         "taxonomy": "Creating",
#         "level": "Hard"
#     }
# ]

import json
from src.core.db_crud import QuestionDB
from config.app_config import AppConfig
app_config = AppConfig()

def import_questions_from_json(json_file_path: str):
    with open(json_file_path, 'r') as file:
        questions = json.load(file)
    return questions

def import_questions_to_db(questions: list[dict]):
    question_db = QuestionDB()
    for question in questions:
        question_db.create(question['question'], question['answer'], question['options'], question['level'], question['taxonomy'])
    question_db.close()

def main():
    questions = import_questions_from_json(app_config.QUESTIONS_JSON_PATH)
    import_questions_to_db(questions)

if __name__ == "__main__":
    main()
