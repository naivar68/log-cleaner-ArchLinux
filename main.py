import os
import sys
from pathlib import Path
import subprocess

def main():
    # Allow root user to access the display server
    subprocess.run(['xhost', 'si:localuser:root'])

    # Switch to Root user
    if os.geteuid() != 0:
        os.execvp('sudo', ['sudo', 'python3'] + sys.argv)

    # Get the home directory of current user
    home_dir = str(Path.home())

    # Shred .bash_history file using bleachbit command
    bash_hist_file = os.path.join(home_dir, "/home/daniel/.bash_history")
    zsh_hist_file = os.path.join(home_dir, "/home/daniel/.zsh_history")
    if os.path.exists(bash_hist_file):
        subprocess.run(['sudo', 'bleachbit', '--shred', bash_hist_file])
        print(f"{bash_hist_file} has been shredded.")
    elif os.path.exists(zsh_history_file):
        subprocess.run(['sudo', 'bleachbit', '--shred', zsh_hist_file])
        print(f"{zsh_hist_file} has been shredded.")
    else:
        print("The history file[s] were not found, please check manually.")

    

    # Get all log files in Arch Linux system and shred them using bleachbit command
    arch_log_files = []
    for root, dirs, files in os.walk("/var/log/journal/5ec7bdfe71194afdb980d2036f822c07"):
        for file in files:
            if "." not in file or (file.endswith(".gz") or file.endswith(".xz")):  # ignore hidden and compressed log files
                continue
            arch_log_files.append(os.path.join(root, file))

    for log_file in arch_log_files:
        subprocess.run(['sudo', 'bleachbit', '--shred', log_file])


if __name__ == "__main__":
    main()
