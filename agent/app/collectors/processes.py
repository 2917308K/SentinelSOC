import psutil


def collect_processes() -> list[dict]:
    """
    Collect information about currently running processes.

    Process information can become unavailable between collection
    attempts, so inaccessible or terminated processes are skipped.
    """

    processes = []

    for process in psutil.process_iter(
        [
            "pid",
            "name",
            "username",
            "cpu_percent",
            "memory_percent",
            "status",
        ]
    ):
        try:
            info = process.info

            processes.append(
                {
                    "pid": info.get("pid"),
                    "name": info.get("name") or "unknown",
                    "username": info.get("username") or "unknown",
                    "cpu_percent": info.get("cpu_percent") or 0.0,
                    "memory_percent": info.get("memory_percent") or 0.0,
                    "status": info.get("status") or "unknown",
                }
            )

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess,
        ):
            continue

    return processes