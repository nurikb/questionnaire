import os
from dotenv import load_dotenv
load_dotenv()

DB_NAME = os.environ["POSTGRES_DBNAME"] if os.environ.get("POSTGRES_DBNAME") else "postgres"
DB_USER = os.environ["POSTGRES_USER"] if os.environ.get("POSTGRES_USER") else "postgres"
DB_PASS = os.environ["POSTGRES_PASS"] if os.environ.get("POSTGRES_PASS") else "postgres"
DB_HOST = os.environ["DB_HOST"] if os.environ.get("DB_HOST") else "db"
DB_PORT = os.environ["DB_PORT"] if os.environ.get("DB_PORT") else "5432"
