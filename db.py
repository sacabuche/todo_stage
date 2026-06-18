import json

class DbTask(object):
    def __init__(self, db_path):
        self.db_path = db_path
        self._data = {
            "counter": 0,
            "current_lang": "en",
            "tasks": []
        }
        self._refresh_from_file()

    def _save_to_file(self, data):
        # Code to save data to the JSON file
        pass    

    def _refresh_from_file(self):
        try:
          with open(self.db_path, 'r', encoding="utf-8") as file:
              self._data = json.load(file)
        except FileNotFoundError:
            pass
        return self._data

    def get_counter(self):
        return self._data.get("counter", 0)

    def get_lang(self):
        return self._data.get("lang", "ES")

    def get_config(self):
        # Code to read configuration from the JSON database
        pass

    def get_all(self):
        return self._data.get("tasks", [])

    def save_all(self):
        # Code to save tasks to the JSON database
        pass

    def add(self, task):
        # Code to add a task to the JSON database
        pass

    def remove(self, task_id):
        # Code to remove a task from the JSON database
        pass
