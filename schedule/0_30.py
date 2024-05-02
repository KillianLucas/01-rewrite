"""
The filename "0_30" refers to:
- 0: Start this script at 0 in Unix time — as in, immediatly.
— 30: Run this script every 30 seconds.

This script sees if any peripherals have been connected. If so, it informs the 01.
"""

import os
import json
import requests
import difflib

# Get the list of connected peripherals
peripherals = os.popen('lsusb').read().split('\n')

# Load previous peripherals from file, or set to empty if file doesn't exist
try:
    with open('peripherals.json', 'r') as f:
        previous_peripherals = json.load(f)
except FileNotFoundError:
    previous_peripherals = []

# If current peripherals differ from previous, send diff to 01 and update file
if peripherals != previous_peripherals:
    diff = list(difflib.unified_diff(previous_peripherals, peripherals))
    if previous_peripherals: # If it's the first run, don't send anything
        requests.post(f"http://localhost:{os.environ['01_PORT']}", data={'diff': diff})
    with open('peripherals.json', 'w') as f:
        json.dump(peripherals, f)
