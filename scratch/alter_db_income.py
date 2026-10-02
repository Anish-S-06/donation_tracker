import sqlite3
import os

def add_income_columns():
    db_path = os.path.join(os.path.dirname(__file__), '..', 'app.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # User columns
    user_cols = [
        ("income_certificate_doc", "VARCHAR(255)"),
        ("income_verification_status", "VARCHAR(20) DEFAULT 'none'")
    ]
    for col_name, col_type in user_cols:
        try:
            c.execute(f"ALTER TABLE users ADD COLUMN {col_name} {col_type}")
            print(f"Added users.{col_name}")
        except sqlite3.OperationalError as e:
            print(f"users.{col_name} check: {e}")

    # Resource columns
    try:
        c.execute("ALTER TABLE resources ADD COLUMN requires_income_proof BOOLEAN DEFAULT 0")
        print("Added resources.requires_income_proof")
    except sqlite3.OperationalError as e:
        print(f"resources.requires_income_proof check: {e}")

    conn.commit()
    conn.close()

if __name__ == '__main__':
    add_income_columns()
