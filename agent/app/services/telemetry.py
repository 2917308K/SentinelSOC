from app.models.event import create_event


def build_system_event(system: dict) -> dict:
    return create_event(
        event_type="SYSTEM",
        hostname=system["hostname"],
        source="sentinel-agent",
        description="Endpoint system information collected.",
        data=system,
    )


def build_metrics_event(
    hostname: str,
    metrics: dict,
) -> dict:
    return create_event(
        event_type="SYSTEM_METRICS",
        hostname=hostname,
        source="sentinel-agent",
        description="Endpoint performance metrics collected.",
        data=metrics,
    )


def build_process_events(
    hostname: str,
    processes: list[dict],
) -> list[dict]:

    return [
        create_event(
            event_type="PROCESS",
            hostname=hostname,
            source="sentinel-agent",
            description=f"Process observed: {process['name']}",
            data=process,
        )
        for process in processes
    ]


def build_network_events(
    hostname: str,
    connections: list[dict],
) -> list[dict]:

    return [
        create_event(
            event_type="NETWORK_CONNECTION",
            hostname=hostname,
            source="sentinel-agent",
            description="Network connection observed.",
            data=connection,
        )
        for connection in connections
    ]