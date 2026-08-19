import psutil


def collect_network_connections() -> list[dict]:
    
    connections = []

    try:
        system_connections = psutil.net_connections(kind="inet")

    except psutil.AccessDenied:
        print(
            "Warning: macOS denied access to system-wide "
            "network connections."
        )
        return connections

    except psutil.Error as exc:
        print(
            f"Warning: unable to collect network connections: {exc}"
        )
        return connections

    for connection in system_connections:
        try:
            local_address = (
                f"{connection.laddr.ip}:{connection.laddr.port}"
                if connection.laddr
                else None
            )

            remote_address = (
                f"{connection.raddr.ip}:{connection.raddr.port}"
                if connection.raddr
                else None
            )

            connections.append(
                {
                    "pid": connection.pid,
                    "status": connection.status,
                    "local_address": local_address,
                    "remote_address": remote_address,
                    "family": str(connection.family),
                    "type": str(connection.type),
                }
            )

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess,
        ):
            continue

    return connections