import json
import psycopg2


# Charger le JSON
with open("tasks.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Connexion PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="Shinka2010"
)

cur = conn.cursor()

# Insérer chaque tâche
for task in data["tasks"]:
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

conn.commit()

cur.close()
conn.close()

print("Import terminé.")