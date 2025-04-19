import os
import re

LOG_DIR = "./logs"
EXPORTER_FILE = "/var/lib/node_exporter/textfile_collector/ueransim.prom"

def parse_logs():
    registration_success = 0
    registration_fail = 0

    for filename in os.listdir(LOG_DIR):
        if filename.endswith(".log"):
            with open(os.path.join(LOG_DIR, filename)) as f:
                content = f.read()
                registration_success += len(re.findall("Registration complete", content))
                registration_fail += len(re.findall("Registration failed", content))

    with open(EXPORTER_FILE, "w") as f:
        f.write(f"ueransim_registration_success {registration_success}\n")
        f.write(f"ueransim_registration_fail {registration_fail}\n")

if __name__ == "__main__":
    parse_logs()
