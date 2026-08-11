import psutil


def collect_system_metrics() -> dict:
   
    memory = psutil.virtual_memory()
    disk = psutil.disk_io_counters()
    network = psutil.net_io_counters()

    return {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory_percent": memory.percent,
        "memory_used": memory.used,
        "memory_available": memory.available,
        "disk_read_bytes": disk.read_bytes if disk else 0,
        "disk_write_bytes": disk.write_bytes if disk else 0,
        "network_bytes_sent": network.bytes_sent if network else 0,
        "network_bytes_received": network.bytes_recv if network else 0,
    }