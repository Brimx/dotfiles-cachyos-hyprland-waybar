#!/bin/bash
# waybar-settings.sh - Rofi UI for Waybar config

CONFIG_FILE="$HOME/.config/waybar/config.jsonc"
CSS_FILE="$HOME/.config/waybar/style.css"
CURRENT_POS=$(grep -oP '"position":\s*"\K[^"]+' "$CONFIG_FILE" 2>/dev/null || echo "top")
CURRENT_AUTOHIDE=$(grep -oP '"mode":\s*"\K[^"]+' "$CONFIG_FILE" 2>/dev/null || echo "none")

CHOICE=$(printf "  Arriba\n  Abajo\n  Bloquear\n  Auto-ocultar\n  Recargar Waybar\n  Salir" | rofi -dmenu -p "Waybar" -theme ~/.config/rofi/themes/luna.rasi)

case "$CHOICE" in
    *Arriba)
        sed -i 's/"position": "[^"]*"/"position": "top"/' "$CONFIG_FILE"
        notify-send "Waybar" "Posición: arriba"
        ;;
    *Abajo)
        sed -i 's/"position": "[^"]*"/"position": "bottom"/' "$CONFIG_FILE"
        notify-send "Waybar" "Posición: abajo"
        ;;
    *Bloquear)
        pkill -STOP waybar
        notify-send "Waybar" "Detenido"
        exit 0
        ;;
    *Auto-ocultar)
        if grep -q '"mode": "invisible"' "$CONFIG_FILE" 2>/dev/null; then
            notify-send "Waybar" "Auto-ocultar desactivado"
        else
            notify-send "Waybar" "Auto-ocultar no configurado aún"
        fi
        exit 0
        ;;
    *Recargar*)
        killall waybar 2>/dev/null
        sleep 0.3
        waybar -c "$CONFIG_FILE" &
        notify-send "Waybar" "Recargado"
        exit 0
        ;;
    *)
        exit 0
        ;;
esac

killall waybar 2>/dev/null
sleep 0.3
waybar -c "$CONFIG_FILE" &
