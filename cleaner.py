#!/usr/bin/env python3

import subprocess
import os
import sys
import time

# Set the path to Bleachbit executable
bleachbit_path = "/usr/bin/bleachbit"

# Define a list of files/folders to clean up
files_to_clean = [
    # Bash history file
    "/home/doctrine/.bash_history",
    # Log files (adjust this list as needed)
    "/var/log/journal/2799311fc98a48e7aaf360bb4746cbf8",  # System log
    "/var/log/samba/*",  # Samba log
    "/var/log/pacman.log",  # Package manager log
    "~/.local/share/trash/*",  # Trash folder
    "~/.cache/*",  # Cache folder
    "/var/tmp/*",  # Temp folder
    "/tmp/*",  # Temp folder
]

command_options = [
    "--clean",  # Start cleaning
    "--overwrite",  # Overwrite files
]


# Check if BleachBit is installed
def bleach():
    # Check if BleachBit executable exists
    if not os.path.exists(bleachbit_path):
        print("Error: BleachBit not found")
        sys.exit(1)

    else:
        print("BleachBit found")
        time.sleep(2)


# Clean up the specified files/folders
def clean_files(folders_to_clean):
    # Expand user paths
    expanded_files = [os.path.expanduser(f) for f in folders_to_clean]

    # Filter out non-existent paths
    valid_files = [f for f in expanded_files if os.path.exists(f)]

    if not valid_files:
        print("Error: No valid files or folders to clean")
        sys.exit(1)

    # Run BleachBit with the specified options and files/folders to clean
    try:
        subprocess.run(
            ['sudo', bleachbit_path] + command_options + valid_files,
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Error: BleachBit failed with error code {e.returncode}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


def main():
    # Engage the user to run the script as root
    subprocess.run("clear" if os.name == "posix" else "cls")
    print("This script must be run as root. 'sudo python3 cleaner.py' to run the script as root.")
    print("If you are not root, close the script now by pressing 'CTRL + C'. Press Enter to continue the script.\n")
    input()
    print("Be careful!! This is a powerful script that will clean up your system files.\n")
    query = input("This script requires root privileges. Continue? [y/n]: ")
    if query.lower() != "y":
        sys.exit(0)
    else:
        bleach()
        clean_files(files_to_clean)


if __name__ == "__main__":
    main()
