from app.collectors.network import collect_network_connections
from app.collectors.processes import collect_processes
from app.collectors.system import collect_system_information
from app.collectors.system_metrics import collect_system_metrics

from app.services.api_client import SentinelAPIClient
from app.services.event_queue import EventQueue
from app.services.telemetry import (
    build_metrics_event,
    build_network_events,
    build_process_events,
    build_system_event,
)


def main():

    print("\n=== SentinelSOC Endpoint Agent ===")

    client = SentinelAPIClient()
    queue = EventQueue()

    system = collect_system_information()

    print("\nRegistering endpoint...")

    registered = client.register_endpoint(
        {
            "agent_id": system["agent_id"],
            "hostname": system["hostname"],
            "operating_system": system["operating_system"],
            "architecture": system["architecture"],
        }
    )

    if registered:
        print("Endpoint registered successfully.")
    else:
        print(
            "Endpoint registration failed."
        )

    queue.add(
        build_system_event(system)
    )

    metrics = collect_system_metrics()

    queue.add(
        build_metrics_event(
            system["hostname"],
            metrics,
        )
    )

    processes = collect_processes()

    queue.add_many(
        build_process_events(
            system["hostname"],
            processes,
        )
    )

    connections = collect_network_connections()

    queue.add_many(
        build_network_events(
            system["hostname"],
            connections,
        )
    )

    print(
        f"\nCollected {queue.size()} events."
    )

    batch_size = 20

    while queue.size() > 0:

        batch = queue.get_batch(batch_size)

        print(
            f"Sending batch of {len(batch)} events..."
        )

        success = client.send_events(batch)

        if not success:

            queue.requeue(batch)

            print(
                "Failed to send batch. "
                "Events returned to queue."
            )

            break

        print("Batch sent successfully.")

    print("\nAgent run completed.")


if __name__ == "__main__":
    main()