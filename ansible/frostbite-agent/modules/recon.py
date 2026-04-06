import os
import socket

def run():
    data = {}

    data["hostname"] = socket.gethostname()
    data["user"] = os.getenv("USER")

    try:
        data["ip"] = socket.gethostbyname(socket.gethostname())
    except:
        data["ip"] = "unknown"

    # running processes
    data["processes"] = os.popen("ps aux --no-heading | head -n 10").read()

    # network info
    data["interfaces"] = os.popen("ip a").read()

    return data
