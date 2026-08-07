import sqlite3
import os

def add_column():
    db_path = os.path.join(os.path.dirname(__file__), '..', 'app.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    try:
        c.execute("ALTER TABLE users ADD COLUMN last_login_ip VARCHAR(45)")
        print("Added last_login_ip column.")
    except sqlite3.OperationalError as e:
        print(f"Error (might already exist): {e}")
    conn.commit()
    conn.close()

if __name__ == '__main__':
    add_column()
