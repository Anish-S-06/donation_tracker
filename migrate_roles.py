import sqlite3

def migrate():
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    
    cursor.execute("UPDATE users SET role = 'user' WHERE role IN ('donor', 'receiver')")
    count = cursor.rowcount
    
    conn.commit()
    conn.close()
    
    print(f"Successfully migrated {count} users to the new 'user' role via raw SQL.")

if __name__ == '__main__':
    migrate()
