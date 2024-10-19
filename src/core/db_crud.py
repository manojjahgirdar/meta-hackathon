import json
import sqlite3

class QuestionDB:
    def __init__(self):
        self.conn = sqlite3.connect('db/questions.db')
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,  
                options TEXT NOT NULL,  
                level TEXT NOT NULL,
                taxonomy TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def create(self, question: str, answer: str, options: dict, level: str, taxonomy: str):
        self.cursor.execute("INSERT INTO questions (question, answer, options, level, taxonomy) VALUES (?, ?, ?, ?, ?)", 
                            (question, answer, json.dumps(options), level, taxonomy))
        self.conn.commit()

    def read(self, id: int):
        self.cursor.execute("SELECT * FROM questions WHERE id=?", (id,))
        return self.cursor.fetchone()   
    
    def read_random(self, difficulty: str, taxonomy: str):
        print(f"Querying for difficulty: {difficulty}, taxonomy: {taxonomy}")
        self.cursor.execute("SELECT * FROM questions WHERE level=? AND taxonomy=? ORDER BY RANDOM() LIMIT 1", (difficulty, taxonomy))
        result = self.cursor.fetchone()
        print(f"Query result: {result}")
        return result
    
    def read_all(self):
        self.cursor.execute("SELECT * FROM questions")
        return self.cursor.fetchall()

    def update(self, id: int, question: str, answer: str, options: dict, level: str, taxonomy: str):
        self.cursor.execute("UPDATE questions SET question=?, answer=?, options=?, level=?, taxonomy=? WHERE id=?", 
                            (question, answer, json.dumps(options), level, taxonomy, id))
        self.conn.commit()

    def delete(self, id: int):
        self.cursor.execute("DELETE FROM questions WHERE id=?", (id,))
        self.conn.commit()  

    def close(self):
        self.conn.close()

