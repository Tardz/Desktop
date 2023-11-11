#!/bin/bash

source /home/jonalm/scripts/rofi/config/config_options.sh 

DMEDITOR="alacritty -e code -n"
choice=$(printf '%s\n' "${display_options[@]}" | rofi -config ~/.config/rofi/files/config.rasi \-theme "$HOME/.config/rofi/files/launchers/type-1"/'style-3-config'.rasi -dmenu -i -l 5 -p '' )
current_screen=$(/home/jonalm/scripts/other/get_current_screen.py)

if [ "$choice" ]; then 
    for option in "${options[@]}"; do
        option_formated=$(echo "$option" | cut -d'-' -f1-1)
        if [[ "$option_formated" == "$choice"* ]]; then
            
            if [ $current_screen -eq 1 ]; then
                # qtile cmd-obj -o cmd -f next_screen
                qtile cmd-obj -o group 1 -f toscreen
                xdotool mousemove --screen 0 900 540
            fi

            cfg=$(echo "${option}" | cut -d'-' -f2- )
            if $DMEDITOR "$cfg"; then
                notify-send -u low -t 3000 '-h' "int:transient:1" "Open config" "<span foreground='#a3be8c' size='medium'>$choice</span>opened in vscode"

            else
                notify-send -u critical -t 3000 '-h' "int:transient:1" "Open config failed" "Error for: <span foreground='#bf616a' size='medium'>$choice</span>"
            fi
        fi
    done
else
    echo "Program terminated." && exit 1
fi

