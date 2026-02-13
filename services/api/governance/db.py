from pathlib import Path
import sqlite3
from config import GOVERNANCE_DB_PATH

DB_PATH = Path(GOVERNANCE_DB_PATH)

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    # Ensure tables exist
    conn.commit()
    conn.close()
