import sqlite3

"""
Given an item, region or solar system, buy or sell, and a price to compare, fetch market data for given location and
compare real-time market data to price point. If market price meets price point's goal, send notification.
"""

DB_NAME_TASKS = "tasks.db"


def get_tasks():
    with sqlite3.connect(DB_NAME_TASKS) as conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM tasks""")

        return cursor.fetchall()

