import os

# Base directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RUNTIME_DIR = os.path.join(BASE_DIR, "runtime")

LEDGER_DIR = os.path.join(RUNTIME_DIR, "ledgers")
KEYS_DIR = os.path.join(RUNTIME_DIR, "keys")
DB_DIR = os.path.join(RUNTIME_DIR, "db")

# Ensure directories exist
os.makedirs(LEDGER_DIR, exist_ok=True)
os.makedirs(KEYS_DIR, exist_ok=True)
os.makedirs(DB_DIR, exist_ok=True)

# Ledger paths
LEDGER_FILE = os.path.join(
    LEDGER_DIR,
    os.getenv("LEDGER_FILE", "ai_firewall_ledger.jsonl")
)

# Key paths
PRIVATE_KEY_PATH = os.path.join(
    KEYS_DIR,
    os.getenv("PRIVATE_KEY_FILE", "ledger_private.key")
)

PUBLIC_KEY_PATH = os.path.join(
    KEYS_DIR,
    os.getenv("PUBLIC_KEY_FILE", "ledger_public.pem")
)

# Database path
GOVERNANCE_DB_PATH = os.path.join(
    DB_DIR,
    os.getenv("GOVERNANCE_DB_FILE", "governance.db")
)

# Grok API Key
GROK_API_KEY = os.getenv("GROK_API_KEY")

# Mode
FIREWALL_MODE = os.getenv("FIREWALL_MODE", "development")

# Backward compatibility
class Settings:
    def __init__(self):
        self.GROK_API_KEY = GROK_API_KEY
        self.LEDGER_FILE = LEDGER_FILE
        self.PRIVATE_KEY_PATH = PRIVATE_KEY_PATH
        self.PUBLIC_KEY_PATH = PUBLIC_KEY_PATH
        self.GOVERNANCE_DB_PATH = GOVERNANCE_DB_PATH
        self.tenant_master_key = os.getenv("TENANT_MASTER_KEY", "dev-master-key")

def get_settings():
    return Settings()
