import json
import os

TASK_FILE = "tasks.json"

def load_tasks():

    if not os.path.exists(TASK_FILE):
        return []

    try:
        with open(TASK_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    except Exception:
        return []

def save_tasks(tasks):

    with open(
        TASK_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            tasks,
            f,
            indent=4,
            ensure_ascii=False
        )