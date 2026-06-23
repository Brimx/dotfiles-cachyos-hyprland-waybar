#!/bin/bash
killall wlogout 2>/dev/null

MONITOR_INFO=$(hyprctl monitors -j | jq '.[] | select(.focused == true)')
WIDTH=$(echo "$MONITOR_INFO" | jq '.width')
HEIGHT=$(echo "$MONITOR_INFO" | jq '.height')

MENU_WIDTH=950
MENU_HEIGHT=160

T_B=$(( (HEIGHT - MENU_HEIGHT) / 2 ))
L_R=$(( (WIDTH - MENU_WIDTH) / 2 ))

wlogout -l ~/.config/wlogout/layout -b 6 -s -T $T_B -B $T_B -L $L_R -R $L_R
