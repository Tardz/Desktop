#!/bin/bash

declare -a options=(
"Floating - add $HOME/.config/qtile/qtile_scripts/update_floating.py"
"Floating - remove $HOME/.config/qtile/qtile_scripts/remove_floating.py"
)

display_options=$(printf '%s\n' "${options[@]}" | cut -d' ' -f1-3)

choice=$(printf '%s\n' "${display_options[@]}" | rofi \-theme "$HOME/.config/rofi/files/launchers/type-1"/'style-3-automation'.rasi -dmenu -i -l 2 -p '' )

if [[ "$choice" == "Quit" ]]; then
    echo "Program terminated." && exit 1
elif [ "$choice" ]; then 
    for option in "${options[@]}"; do
        option_formated=$(echo "$option" | cut -d' ' -f1-3)
        if [[ "$option_formated" == "$choice"* ]]; then
            file_path=$(echo "$option" | cut -d' ' -f4- )
            echo "$file_path" 
            python3 "$file_path"
            break
        fi
    done
else
    echo "Program terminated." && exit 1
fi