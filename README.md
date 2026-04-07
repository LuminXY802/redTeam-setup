# Project Frostbite: The combination of red tools I made and cooked up

# Overview
Project Frostbite is a Red Team infrastructure suite I built for the “Cold War” competition environment. The goal was to bridge the gap between getting initial access and actually maintaining it, without having to manually piece everything together mid-comp.

Instead of relying on a bunch of separate tools, this setup combines automated situational awareness with a more flexible exfiltration approach. The idea is simple: get in, figure out what works for outbound traffic, and make sure you can always get data back out—even if things start getting blocked.

### Core Components:
1. **Frostbite Agent:** A modular Python3 agent that pulls useful artifacts like SSH keys and `.bash_history` right away.
2. **Egress Hunting:** Logic that tests common outbound ports (443, 80, 8080) instead of relying on a single hardcoded connection path.
3. **Moscow Fallback:** A DNS-based backup channel using `dnscat2` when normal traffic gets shut down.
4. **Sliver C2:** Used for full command-and-control once a stable foothold is established.

---

## Installation & Deployment

This whole setup is automated through **Ansible**, so you don’t have to manually configure the jump box.

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/LuminXY802/redTeam-setup
    cd RedTeam-Tools
    ```

2. **Run the Playbook:**
    ```bash
    ansible-playbook setup-redteam.yml --ask-become-pass
    ```

3. **Verify Setup:**
    After logging in, you should see the **Lake Placid 1980 MOTD** and have access to the custom global commands.

---

## Operational Commands (The Toolkit)

These commands are set up globally so you can move fast without worrying about paths:

| Command | Action |
| :--- | :--- |
| `score_goal` | Launches the **Sliver C2** server console |
| `view_loot` | Starts a Netcat listener on **Port 443** for Frostbite data |
| `call_moscow` | Frees up Port 53 and starts the **dnscat2** DNS server |
| `situational_awareness` | Runs **LinPEAS** for deeper privilege escalation recon |
| `frostbite` | Runs a local test of the **Frostbite Agent** |

---

## Usage Workflow

1. **Preparation:**  
   Start a listener with `view_loot` (preferably in a tmux pane) so you’re ready to catch incoming data.

2. **Infiltration:**  
   Transfer `frostbite_agent.py` to the target machine using whatever method you have available (SCP, curl, etc.).

3. **Exfiltration:**  
   Run the agent:
   ```bash
   python3 frostbite_agent.py
