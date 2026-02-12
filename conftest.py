import os

# Ensure key exists before any module import
if "TENANT_MASTER_KEY" not in os.environ:
    os.environ["TENANT_MASTER_KEY"] = "PWquANGz7JF-n9n4C5Fgk44DSva5YKZK2KOzCVSQfDc="
