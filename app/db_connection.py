import os
import psycopg2
from dotenv import load_dotenv
#loading variables from .env file
load_dotenv()
#connecting db
DATABASE_URL = os.getenv("DATABASE_URL")
def get_connection():
    return psycopg2.connect(DATABASE_URL)