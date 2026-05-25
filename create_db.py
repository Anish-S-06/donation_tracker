import pymysql

def create_db():
    passwords_to_try = ['', 'root', 'password']
    
    for pwd in passwords_to_try:
        try:
            print(f"Attempting to connect to MariaDB with password '{pwd}'...")
            connection = pymysql.connect(host='localhost', user='root', password=pwd)
            with connection.cursor() as cursor:
                cursor.execute("CREATE DATABASE IF NOT EXISTS donation_tracker_db")
            connection.commit()
            connection.close()
            print("SUCCESS! Database 'donation_tracker_db' has been created.")
            
            # Update config.py with the correct password
            with open('config.py', 'r') as f:
                content = f.read()
            
            old_uri = "mysql+pymysql://root:password@localhost/donation_tracker_db"
            new_uri = f"mysql+pymysql://root:{pwd}@localhost/donation_tracker_db"
            
            if old_uri in content:
                with open('config.py', 'w') as f:
                    f.write(content.replace(old_uri, new_uri))
                print("Updated config.py with the correct password.")
            
            return True
        except Exception as e:
            print(f"Failed: {e}")
            
    print("Could not connect to MariaDB using default passwords.")
    return False

if __name__ == '__main__':
    create_db()
