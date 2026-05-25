import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-default-key-for-dev'
    
    basedir = os.path.abspath(os.path.dirname(__file__))
    
    # We will use SQLite for local development temporarily
    # To switch back to MariaDB later, just change this URI.
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
