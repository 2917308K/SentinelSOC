import json

from app.collectors.network import collect_network_connections
from app.collectors.processes import collect_processes
from app.collectors.system import collect_system_information
from app.collectors.system_metrics import collect_system_metrics


def main():
    system = collect_system_information()

    print("\n=== SentinelSOC Endpoint Agent ===")

    print("\nSystem:")
    print(json.dumps(system, indent=2))

    print("\nSystem Metrics:")
    print(
        json.dumps(
            collect_system_metrics(),
            indent=2,
        )
    )

    print("\nProcesses:")

    processes = collect_processes()

    for process in processes[:20]:
        pid = process.get("pid")
        name = process.get("name") or "unknown"
        cpu = process.get("cpu_percent") or 0.0
        memory = process.get("memory_percent") or 0.0

        print(
            f"{str(pid):>6} "
            f"{name:<30.30} "
            f"CPU={cpu:<6.1f} "
            f"MEM={memory:<6.1f}"
    )

    print("\nNetwork Connections:")

    connections = collect_network_connections()

    for connection in connections[:20]:
        print(json.dumps(connection, indent=2))


if __name__ == "__main__":
    main()