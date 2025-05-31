import os
import sys
from pathlib import Path
import subprocess

def main():
    # Allow root user to access the display server
    subprocess.run(['xhost', 'si:localuser:root'])

    # Switch to root user if not already
    if os.geteuid() != 0:
        os.execvp('sudo', ['sudo', sys.executable] + sys.argv)

    # Get the home directory of the current user
    home_dir = str(Path.home())

    # List of history files to shred
    history_files = [
        os.path.join(home_dir, '.bash_history'),
        os.path.join(home_dir, '.zsh_history')
    ]

    found = False
    for hist_file in history_files:
        if os.path.exists(hist_file):
            subprocess.run(['bleachbit', '--shred', hist_file])
            print(f"{hist_file} has been shredded.")
            found = True

    if not found:
        print("No history files found, please check manually.")

    # Shred all log files in /var/log and /var/log/journal
    log_dirs = ['/var/log', '/var/log/journal']
    log_files = []
    for log_dir in log_dirs:
        for root, dirs, files in os.walk(log_dir):
            for file in files:
                file_path = os.path.join(root, file)
                log_files.append(file_path)

    for log_file in log_files:
        subprocess.run(['bleachbit', '--shred', log_file])

if __name__ == "__main__":
    main()
