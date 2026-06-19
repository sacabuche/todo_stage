import json

import psycopg2
from psycopg2.extras import DictCursor

class DbTask(object):
    def __init__(self):
        self._data = {
            "config": {
                "conter": 0,
                "current_lang": "EN"
            },
            "tasks": []
        }
        self.db = psycopg2.connect(
          host="localhost",
          database="postgres",
          user="postgres",
          password="Shinka2010"
        )

    def _save_to_file(self, data):
        # Code to save data to the JSON file
        pass    

    def get_counter(self):
        return self.get_config().get("counter", 0)
    
    def get_lang(self):
        return self.get_config().get("current_lang", "ES")
    
    def save_counter(self, counter):
        self._data["config"]["counter"] = counter
        self._save_to_file(self._data)  
    
    def save_lang(self, lang):
        self._data["config"]["current_lang"] = lang
        self._save_to_file(self._data)

    def get_config(self):
        return self._data.get("config", {})

    def get_all(self):
        cur = self.db.cursor(cursor_factory=DictCursor)
        cur.execute("SELECT * FROM tasks")
        rows = cur.fetchall()
        cur.close()
        return rows

    def add(self, task):
        cur = self.db.cursor()
        cur.execute(
            """
            INSERT INTO tasks (text, "group", done, priority, tag)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                task["text"],
                task["group"],
                task["done"],
                task["priority"],
                task["tag"]
            )
        )
        self.db.commit()
        cur.close()

    def remove(self, task_id):
        cur = self.db.cursor()
        cur.execute("DELETE FROM tasks WHERE tag = %s", (task_id,))
        self.db.commit()
        cur.close()
        return self.get_all()
