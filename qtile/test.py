#!/usr/bin/env python

import subprocess
import sys

output = subprocess.check_output(["xrandr", "-q"]).decode().strip()
data = subprocess.check_output(['awk', '/HDMI-0|DVI-D-0/ {print $1 ": " $2}'], input=output.encode()).decode().strip()
print(data)