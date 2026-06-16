from dataclasses import dataclass, asdict

@dataclass
class Task:
    title: str
    completed: bool = False
    favorite: bool = False
    priority: str = "Medium"
    due_date: str = ""

    def to_dict(self):
        return asdict(self)