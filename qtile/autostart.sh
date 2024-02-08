#!/bin/bash
### DISPLAY CONF ###
xrandr --output DisplayPort-0 --mode 1920x1080 --rate 144 --pos 0x0 --output DisplayPort-2 --mode 1920x1080 --rate 144 --pos 1920x0 --output HDMI-A-0 --off

### KEYBOARD CONF ###
setxkbmap se

### APPS ###
nitrogen --restore
picom --blur-method dual_kawase &
openrazer-daemon
imwheel -b 45
polychromatic-cli --dpi 600

killall alttab
background_path=$(awk -F'=' '/file=/{print $2}' ~/.config/nitrogen/bg-saved.cfg)
sudo cp $background_path /usr/share/sddm/themes/sugar-candy/background.png
alttab -bg '#2e3440' -fg '#d8dee9' -bc '#2e3440' -bw 18 -inact '#3b4252' -frame '#81a1c1' &