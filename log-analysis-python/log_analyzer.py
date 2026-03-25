"""
Log Analysis Tool – Detecting Failed SSH Login Attempts

This script analyzes authentication logs and detects repeated failed login attempts
from the same IP address, which may indicate a brute-force attack.

Usage:
python log_analyzer.py auth.log
"""

import re
import sys
from collections import Counter


# Regex pattern to capture IP address after the word "from"
pattern = r"from (\d+\.\d+\.\d+\.\d+)"


def analyze_log(file_path):

    failed_ips = []

    # Open and read the log file
    with open(file_path, "r") as file:
        lines = file.readlines()

    # Extract IP addresses from failed login attempts
    for line in lines:
        if "Failed password" in line:

            match = re.search(pattern, line)

            if match:
                failed_ips.append(match.group(1))

    # Count occurrences of IP addresses
    counter = Counter(failed_ips)

    print("\nFailed login attempts by IP:\n")

    for ip, count in counter.items():
        print(f"{ip}: {count}")

    print("\nPossible brute force attempts:\n")

    for ip, count in counter.items():
        if count > 3:
            print(f"⚠ Possible brute force from {ip} ({count} attempts)")


# CLI argument handling
if len(sys.argv) != 2:
    print("Usage: python log_analyzer.py <logfile>")
    sys.exit(1)

log_file = sys.argv[1]

analyze_log(log_file)
