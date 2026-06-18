import json

class DbTask(object):
    def __init__(self, db_path):
        self.db_path = db_path
        self._data = {
            "config": {
                "conter": 0,
                "current_lang": "en"
            },
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
        return self._data.get("tasks", [])

    def add(self, task):
        # append to the current tasks
        # save the all the task together
        # return current tasks
        pass

    def remove(self, task_id):
        # Code to remove a task from the JSON database
        pass
