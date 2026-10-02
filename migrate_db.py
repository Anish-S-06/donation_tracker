import os
import sys

# Ensure project root is in python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app, db
from sqlalchemy import inspect, text

def run_migration():
    print("Initializing Flask App...")
    app = create_app()
    with app.app_context():
        print(f"Connected to database URI: {app.config.get('SQLALCHEMY_DATABASE_URI')}")
        insp = inspect(db.engine)
        existing_tables = insp.get_table_names()
        print(f"Existing tables: {existing_tables}")

        if not existing_tables:
            print("No tables found. Creating all tables from models...")
            db.create_all()
            print("All tables created successfully!")
            return

        # Users table migrations
        if 'users' in existing_tables:
            user_cols = {c['name'] for c in insp.get_columns('users')}
            new_user_cols = [
                ('last_login_ip', 'VARCHAR(45)'),
                ('darpan_id', 'VARCHAR(50)'),
                ('org_pan', 'VARCHAR(20)'),
                ('pan_card_doc', 'VARCHAR(255)'),
                ('auth_letter_doc', 'VARCHAR(255)'),
                ('income_certificate_doc', 'VARCHAR(255)'),
                ('income_verification_status', "VARCHAR(20) DEFAULT 'none'")
            ]
            with db.engine.begin() as conn:
                for col_name, col_type in new_user_cols:
                    if col_name not in user_cols:
                        conn.execute(text(f"ALTER TABLE users ADD COLUMN {col_name} {col_type}"))
                        print(f" -> Added column: users.{col_name}")
                    else:
                        print(f" -> users.{col_name} already exists.")

        # Resources table migrations
        if 'resources' in existing_tables:
            res_cols = {c['name'] for c in insp.get_columns('resources')}
            with db.engine.begin() as conn:
                if 'requires_income_proof' not in res_cols:
                    conn.execute(text("ALTER TABLE resources ADD COLUMN requires_income_proof BOOLEAN DEFAULT 0"))
                    print(" -> Added column: resources.requires_income_proof")
                else:
                    print(" -> resources.requires_income_proof already exists.")

        print("\nDatabase migration completed successfully!")

if __name__ == '__main__':
    run_migration()
