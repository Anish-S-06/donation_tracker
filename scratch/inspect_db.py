import sqlite3, os

db_path = 'app.db'
if not os.path.exists(db_path):
    print("Searching for db files...")
    for root, dirs, files in os.walk('.'):
        for f in files:
            if f.endswith('.db') or f.endswith('.sqlite'):
                print(os.path.join(root, f))
else:
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [t[0] for t in cur.fetchall() if not t[0].startswith('sqlite_')]
    print("Tables found:", tables)
    for t in tables:
        cur.execute(f"SELECT COUNT(*) FROM {t}")
        cnt = cur.fetchone()[0]
        cur.execute(f"PRAGMA table_info({t});")
        cols = [c[1] for c in cur.fetchall()]
        print(f"\n--- Table: {t} (Count: {cnt}) ---")
        print("Columns:", cols)
        cur.execute(f"SELECT * FROM {t} LIMIT 5")
        rows = cur.fetchall()
        for r in rows:
            print("Row:", r)
