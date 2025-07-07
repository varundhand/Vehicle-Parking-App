import os
import secrets # for generating secure tokens for csrf protection

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'parking.db')}"

# BASE_DIR gives the backend folder's full path.

# DATABASE_URL creates the SQLite connection string.

# This is used by Flask to know where the database file should be.

#* BEFORE
# SECRET_KEY = "supersecretkey"  # You can use os.urandom(24).hex() for stronger key
# JWT_SECRET_KEY = "superjwtsecret"

#* AFTER
SECRET_KEY = secrets.token_urlsafe(32)
JWT_SECRET_KEY = secrets.token_urlsafe(32)