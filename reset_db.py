import os, sqlite3
db_path = os.path.join(os.path.dirname(__file__), "data", "jobs.db")
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    conn.execute("DROP TABLE IF EXISTS jobs")
    conn.commit()
    conn.close()
    print(f"Cleared database at {db_path}")
else:
    print("No database found")
