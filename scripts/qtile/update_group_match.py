#!/usr/bin/env python

import re
import subprocess

# Use xprop to get the WM_CLASS property of the window
p = subprocess.Popen(['xprop', '-notype', 'WM_CLASS'], stdout=subprocess.PIPE)
out, _ = p.communicate()

# Extract the WM_CLASS value from the output
wm_class = str(out).split('"')[1]

# Read the existing qtile config file
with open('/home/jonalm/.config/qtile/config.py', 'r') as f:
    config_lines = f.readlines()

data = subprocess.check_output(["qtile", "cmd-obj", "-o", "group", "-f", "info"]).decode().strip()
match = re.search(r"'name': '(\d+)'", data)

if match:
    group = match.group(1)
else:
    print("group not found. Error: ", match)
    exit(1)

for i, line in enumerate(config_lines):
    # Search for the line you're interested in
    if f'            Match(wm_class = ["{wm_class}"]),' in line:
        # If the line is found, print the index and the line itself
        print("Wm class already exists!")
        exit(1)

for i, line in enumerate(config_lines):
    # Search for the line you're interested in
    if f"Group('{match.group(1)}'," in line:
        # If the line is found, print the index and the line itself
        print(f"Line {i}: {line}")
        break

# Find the index of the floating_layout line
start_i = i + 1

# Add the new match rule to the float_rules list
new_line = f'            Match(wm_class = ["{wm_class}"]),\n'
config_lines.insert(start_i, new_line)

# Write the updated config file
with open('/home/jonalm/.config/qtile/config.py', 'w') as f:
    f.writelines(config_lines)

# # Restart qtile
subprocess.run(["qtile", "cmd-obj", "-o", "cmd", "-f", "restart"])