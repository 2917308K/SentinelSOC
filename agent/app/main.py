from app.collectors.network import collect_network_connections
from app.collectors.processes import collect_processes
from app.collectors.system import collect_system_information
from app.collectors.system_metrics import collect_system_metrics
from app.services.api_client import SentinelAPIClient


def main():

    system = collect_system_information()

    print("\n=== SentinelSOC Endpoint Agent ===")

    print("\nRegistering endpoint...")

    client = SentinelAPIClient()

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
            "Endpoint registration failed. "
            "Continuing in local collection mode."
        )

    print("\nSystem:")
    print(system)

    print("\nSystem Metrics:")
    print(collect_system_metrics())

    print("\nProcesses:")

    processes = collect_processes()

    for process in processes[:20]:
        print(
            f"{process['pid']:>6} "
            f"{process['name']:<30} "
            f"CPU={process['cpu_percent']:<6} "
            f"MEM={process['memory_percent']:<6}"
        )

    print("\nNetwork Connections:")

    connections = collect_network_connections()

    for connection in connections[:20]:
        print(connection)


if __name__ == "__main__":
    main()