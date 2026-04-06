import os

def run():
    cron_job = "*/5 * * * * python3 /opt/red-tools/frostbite_agent.py\n"

    try:
        with open("/tmp/frostbite_cron", "w") as f:
            f.write(cron_job)

        os.system("crontab /tmp/frostbite_cron")
    except:
        pass
