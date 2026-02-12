import os
from functools import lru_cache


class Settings:
    def __init__(self):
        self.tenant_master_key = os.getenv("TENANT_MASTER_KEY")
        self.enable_governance = os.getenv("ENABLE_GOVERNANCE", "true").lower() == "true"
        self.environment = os.getenv("ENVIRONMENT", "production")


@lru_cache()
def get_settings() -> Settings:
    return Settings()
