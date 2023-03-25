#!/bin/bash
### DISPLAY CONF ###
#xrandr --output DVI-D-1  --mode 1920x1080 --rate 144 --output HDMI-1 --mode 1920x1080 --rate 144
#xrandr --output DVI-D-1 --mode 1920x1080 --rate 144.01 --left-of HDMI-1 --output HDMI-1 --mode 1920x1080 --rate 144.00

#xrandr --output DVI-I-0 --off 
#xrandr --output DVI-I-1 --off 
#xrandr --output HDMI-0 --off
#xrandr --output DP-0 --off
#xrandr --output DP-1 --mode 1920x1080 --pos 0x0 --rotate normal --rate 144 
xrandr --output DP-1 --off 
xrandr --output HDMI-0 --mode 1920x1080 --rotate normal --rate 144
xrandr --output DVI-D-0 --primary --mode 1920x1080 --pos 0x0 --rotate normal --rate 144

# xrandr --output DVI-D-0 --off
# #xrandr --output HDMI-1 --off
# xrandr --output DVI-D-0 --mode 1920x1080 --rate 144 
# xrandr --output HDMI-1 --mode 1920x1080 --rate 144

#--right-of HDMI-1
### KEYBOARD CONF ###
setxkbmap se

### APPS ###
#alttab --restore
nitrogen --restore &
emacs --daemon &
openrazer-daemon
imwheel -b 45 &
#picom --experimental-backends --backend glx &
picom -b &
unclutter -idle 2 &
#nm-applet &
#polychromatic-tray-applet &
#blueman-applet &
