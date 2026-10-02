import sqlite3
import os

def migrate_all():
    db_path = os.path.join(os.path.dirname(__file__), '..', 'app.db')
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}")
        return

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Columns for 'users' table
    user_columns = [
        ("last_login_ip", "VARCHAR(45)"),
        ("darpan_id", "VARCHAR(50)"),
        ("org_pan", "VARCHAR(20)"),
        ("pan_card_doc", "VARCHAR(255)"),
        ("auth_letter_doc", "VARCHAR(255)"),
        ("income_certificate_doc", "VARCHAR(255)"),
        ("income_verification_status", "VARCHAR(20) DEFAULT 'none'")
    ]

    for col_name, col_type in user_columns:
        try:
            c.execute(f"ALTER TABLE users ADD COLUMN {col_name} {col_type}")
            print(f"Added users.{col_name}")
        except sqlite3.OperationalError as e:
            print(f"users.{col_name}: {e}")

    # Columns for 'resources' table
    resource_columns = [
        ("requires_income_proof", "BOOLEAN DEFAULT 0")
    ]

    for col_name, col_type in resource_columns:
        try:
            c.execute(f"ALTER TABLE resources ADD COLUMN {col_name} {col_type}")
            print(f"Added resources.{col_name}")
        except sqlite3.OperationalError as e:
            print(f"resources.{col_name}: {e}")

    conn.commit()
    conn.close()
    print("Migration completed successfully!")

if __name__ == '__main__':
    migrate_all()
