#!/bin/bash

BROWSER="brave"

source /home/jonalm/scripts/rofi/search/search_options.sh 

while [ -z "$engine" ]; do
    displayname=$(printf '%s\n' "${display_options[@]}" | rofi \-theme "$HOME/.config/rofi/files/launchers/type-1"/'style-7'.rasi -dmenu -i -l 6 -p '') || exit
    engine=$(echo "$options" | cut -d' ' -f1-1)
done

for option in "${options[@]}"; do
    option_formated=$(echo "$option" | cut -d'-' -f1-1)
    if [[ "$displayname" == "$option_formated" ]]; then
        url=$(echo "$option" | cut -d'-' -f2- )
        search=$(echo "$option" | cut -d' ' -f2)
        if [[ "$search" == "Search" ]]; then
            while [ -z "$query" ]; do
                query=$(rofi \-theme "$HOME/.config/rofi/files/launchers/type-1"/'style-7-search'.rasi -dmenu -i -l 2 -p '') || exit
            done
            if [[ "$qtile_info" == *"'screen': 1"* ]]; then
                echo "screen 1"
                qtile cmd-obj -o group 2 -f toscreen
            else
                echo "screen 2"
                qtile cmd-obj -o cmd -f next_screen
                qtile cmd-obj -o group 2 -f toscreen
            fi
            $BROWSER "$url""$query"
            exit 1
        fi
    fi
done

if [[ "$qtile_info" == *"'screen': 1"* ]]; then
    echo "screen 1 a"
    qtile cmd-obj -o group 2 -f toscreen
else
    echo "screen 2 a"
    qtile cmd-obj -o cmd -f next_screen
    qtile cmd-obj -o group 2 -f toscreen
fi
$BROWSER "$url"
exit 1

