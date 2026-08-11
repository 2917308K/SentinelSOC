import os
import secrets
from fastapi import Header, HTTPException, status


AGENT_API_KEY = os.getenv(
    "SENTINELSOC_AGENT_API_KEY",
)


def verify_agent_api_key(
    x_agent_key: str | None = Header(default=None),
) -> None:

    if not AGENT_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Agent authentication is not configured.",
        )

    if not x_agent_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing agent API key.",
        )

    if not secrets.compare_digest(
        x_agent_key,
        AGENT_API_KEY,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid agent API key.",
        )