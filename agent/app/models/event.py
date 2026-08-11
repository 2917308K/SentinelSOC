from datetime import datetime, timezone


def create_event(
    *,
    event_type: str,
    hostname: str,
    source: str,
    description: str,
    data: dict,
) -> dict:
    

    return {
        "event_type": event_type,
        "severity": "INFO",
        "source": source,
        "hostname": hostname,
        "username": None,
        "description": description,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "data": data,
    }