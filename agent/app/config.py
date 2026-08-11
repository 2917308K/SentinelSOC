import os


API_URL = os.getenv(
    "SENTINELSOC_API_URL",
    "http://127.0.0.1:8000",
)

AGENT_ID = os.getenv(
    "SENTINELSOC_AGENT_ID",
    "development-agent",
)

AGENT_API_KEY = os.getenv(
    "SENTINELSOC_API_KEY",
    "",
)

BATCH_SIZE = int(
    os.getenv(
        "SENTINELSOC_BATCH_SIZE",
        "20",
    )
)