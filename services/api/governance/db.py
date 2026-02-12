import sqlite3
from pathlib import Path

DB_PATH = Path("governance.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA foreign_keys=ON;")
    return conn

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS governance_policy (
        id TEXT PRIMARY KEY,
        action_type TEXT NOT NULL,
        tenant_id TEXT,
        layers_json TEXT NOT NULL,
        expires_in_seconds INTEGER,
        cooldown_seconds INTEGER,
        version INTEGER NOT NULL,
        policy_hash TEXT NOT NULL,
        signature TEXT NOT NULL,
        created_at INTEGER NOT NULL
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS approver_registry (
        approver_id TEXT PRIMARY KEY,
        role TEXT NOT NULL,
        public_key TEXT NOT NULL,
        status TEXT NOT NULL,
        valid_from INTEGER,
        valid_until INTEGER,
        registry_signature TEXT NOT NULL
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS governance_action (
        id TEXT PRIMARY KEY,
        action_type TEXT NOT NULL,
        tenant_id TEXT,
        payload_hash TEXT NOT NULL,
        status TEXT NOT NULL,
        current_layer INTEGER NOT NULL,
        expires_at INTEGER,
        cooldown_until INTEGER,
        consumed INTEGER DEFAULT 0,
        created_at INTEGER NOT NULL
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS approval (
        id TEXT PRIMARY KEY,
        action_id TEXT NOT NULL,
        layer_index INTEGER NOT NULL,
        approver_id TEXT NOT NULL,
        role TEXT NOT NULL,
        signature TEXT NOT NULL,
        timestamp INTEGER NOT NULL,
        FOREIGN KEY(action_id) REFERENCES governance_action(id)
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS governance_audit (
        id TEXT PRIMARY KEY,
        action_id TEXT,
        event_type TEXT NOT NULL,
        data_json TEXT NOT NULL,
        previous_hash TEXT,
        current_hash TEXT NOT NULL,
        timestamp INTEGER NOT NULL
    );
    """)

    conn.commit()
    conn.close()
