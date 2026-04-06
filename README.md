# Project Frostbite: The combination of red tools I made and cooked up

# Overview
Project Frostbite is a specialized Red Team infrastructure suite designed for the "Cold War" competition environment. It bridges the gap between initial access and long-term persistence by combining automated situational awareness with a resilient, multi-protocol exfiltration engine.

### Core Components:
1.  **Frostbite Agent:** A modular Python3 agent that harvests SSH keys and bash history.
2.  **Egress Hunting:** Intelligent exfiltration logic that tests TCP 443, 80, and 8080 before falling back to DNS.
3.  **Moscow Fallback:** An emergency DNS tunnel (via `dnscat2`) for "deny-all" firewall environments.
4.  **Sliver C2:** Integration with the Sliver framework for interactive command and control.

---

## Installation & Deployment

This project is fully automated via **Ansible**. To set up the Red Team Jump Box:

1.  **Clone the Repository:**
    ```bash
    git clone [Your-GitHub-Link]
    cd RedTeam-Tools
    ```

2.  **Run the Playbook:**
    ```bash
    ansible-playbook site.yml --ask-become-pass
    ```

3.  **Verify Setup:**
    Upon login, you should see the **Lake Placid 1980 MOTD** and have access to the custom global commands.

---

## Operational Commands (The Toolkit)

The following aliases are configured globally to simplify high-stress operations:

| Command | Action |
| :--- | :--- |
| `score_goal` | Launches the **Sliver C2** Server console. |
| `view_loot` | Starts a Netcat listener on **Port 443** to catch Frostbite data. |
| `call_moscow` | Clears Port 53 and starts the **dnscat2** DNS tunnel server. |
| `situational_awareness` | Executes **LinPEAS** for deep-dive privilege escalation recon. |
| `frostbite` | Runs a local test of the **Frostbite Agent**. |

---

## Usage Workflow

1.  **Preparation:** Run `view_loot` in a `tmux` pane to wait for incoming data.
2.  **Infiltration:** Deploy `frostbite_agent.py` to the target machine via your preferred method (SCP, Curl, or Ansible).
3.  **Exfiltration:** Run the agent: `python3 frostbite_agent.py`.
4.  **Escalation:** If TCP exfiltration fails, run `call_moscow` on the Jump Box to catch the DNS fallback stream.
5.  **Control:** Once credentials are recovered, use `score_goal` to deploy a full Sliver implant for persistence.

---

## Troubleshooting

- **Port 53 Busy:** The `call_moscow` command automatically attempts to stop `systemd-resolved`. If it fails, run `sudo fuser -k 53/udp`.
- **JSON Formatting:** If `view_loot` output is messy, ensure `jq` is installed (the Ansible script should handle this).
- **Permissions:** Ensure the agent is executable: `chmod +x frostbite_agent.py`.

---

*“Preparation is the only tool that never dulls.” — Lake Placid Operational Manual, 1980*
