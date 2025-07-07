import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'parking.db')}"

# BASE_DIR gives the backend folder's full path.

# DATABASE_URL creates the SQLite connection string.

# This is used by Flask to know where the database file should be.