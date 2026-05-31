import sqlite3

conn = sqlite3.connect("tasks.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    priority TEXT,
    due_date TEXT,
    status TEXT
)
""")
conn.commit()

def add_task(name, priority, due_date):
    cursor.execute(
        "INSERT INTO tasks (name, priority, due_date, status) VALUES (?, ?, ?, ?)",
        (name, priority, due_date, "Pending")
    )
    conn.commit()

def get_tasks():
    cursor.execute("SELECT * FROM tasks")
    return cursor.fetchall()

def update_task(task_id, name):
    cursor.execute("UPDATE tasks SET name=? WHERE id=?", (name, task_id))
    conn.commit()

def update_status(task_id, status):
    cursor.execute("UPDATE tasks SET status=? WHERE id=?", (status, task_id))
    conn.commit()

def delete_task(task_id):
    cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()