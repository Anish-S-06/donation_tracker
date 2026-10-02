import sqlite3
import os

def add_ngo_columns():
    db_path = os.path.join(os.path.dirname(__file__), '..', 'app.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    columns = [
        ("darpan_id", "VARCHAR(50)"),
        ("org_pan", "VARCHAR(20)"),
        ("pan_card_doc", "VARCHAR(255)"),
        ("auth_letter_doc", "VARCHAR(255)")
    ]
    for col_name, col_type in columns:
        try:
            c.execute(f"ALTER TABLE users ADD COLUMN {col_name} {col_type}")
            print(f"Added {col_name} column.")
        except sqlite3.OperationalError as e:
            print(f"Column {col_name} check: {e}")
    conn.commit()
    conn.close()

if __name__ == '__main__':
    add_ngo_columns()
