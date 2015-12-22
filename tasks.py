import sqlite3

DB_NAME_TASKS = "tasks.db"


def get_tasks():
    with sqlite3.connect(DB_NAME_TASKS) as conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM tasks""")

        return cursor.fetchall()
