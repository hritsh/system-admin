#!/usr/bin/env python3
"""
Name: Hritish Mahajan
Date: 1 May 2023
"""


import os
import re
from collections import Counter
from datetime import datetime
from geoip import geolite2

def colorize(text, color="green"):
    """Colorize text"""
    color = {'green': '\033[92m', 'red': '\033[91m',
             'yellow': '\033[93m', 'underline': '\033[4m\033[33m'}[color]
    return color + text + '\033[0m'

# Clear the terminal
os.system('clear' if os.name == 'posix' else 'cls')

# Read the syslog.log file
with open("syslog.log", "r") as file:
    log_data = file.read()

# Regex to find IP addresses with failed login attempts
ip_pattern = re.compile(
    r'Failed password for .* from (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')

# Find IP addresses in the log data
ip_addresses = ip_pattern.findall(log_data)

# Count the occurrences of each IP address
ip_count = Counter(ip_addresses)

# Filter IP addresses with 10 or more failed attempts
filtered_ip_count = {ip: count for ip,
                     count in ip_count.items() if count >= 10}

# Sort the IP addresses by count in ascending order
sorted_ip_count = sorted(filtered_ip_count.items(), key=lambda x: x[1])

# Print the report header
print(colorize("Attacker Report - ") + datetime.now().strftime('%B %d, %Y'))
print(colorize("\nCOUNT\tIP ADDRESS\tCOUNTRY", "red"))

# Print the report data
for ip, count in sorted_ip_count:
    country = geolite2.lookup(ip)
    if country is not None:
        country_code = country.country
    else:
        country_code = "Unknown"
    print(f"{count}\t{ip}\t{country_code}")

# Close the geolite2 reader to release resources
print()
geolite2.close()
