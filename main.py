import os
from pathlib import Path
import subprocess

def main():
    # Get the home directory of current user
    home_dir = str(Path.home())

    # Shred .bash_history file using bleachbit command
    bash_hist_file = os.path.join(home_dir, ".bash_history")
    if os.path.exists(bash_hist_file):
        subprocess.run(['sudo', 'bleachbit', '--shred', bash_hist_file])

    # Get all log files in Arch Linux system and shred them using bleachbit command
    arch_log_files = []
    for root, dirs, files in os.walk("/var/log"):
        for file in files:
            if "." not in file or (file.endswith(".gz") or file.endswith(".xz")):  # ignore hidden and compressed log files
                continue
            arch_log_files.append(os.path.join(root, file))

    for log_file in arch_log_files:
        subprocess.run(['sudo', 'bleachbit', '--shred', log_file])

if __name__ == "__main__":
    main()

