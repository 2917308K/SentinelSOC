import platform
import socket
import uuid


def collect_system_information() -> dict:
   
    return {
        "hostname": socket.gethostname(),
        "operating_system": platform.system(),
        "os_version": platform.version(),
        "architecture": platform.machine(),
        "processor": platform.processor(),
        "agent_id": str(uuid.getnode()),
    }