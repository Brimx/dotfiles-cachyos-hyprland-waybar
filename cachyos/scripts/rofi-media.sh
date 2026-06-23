#!/bin/bash

PLAYER=$(playerctl -l 2>/dev/null | head -1)
if [ -z "$PLAYER" ]; then
    notify-send "  Media" "No hay reproductores activos"
    exit 1
fi

STATUS=$(playerctl status 2>/dev/null)
TITLE=$(playerctl metadata title 2>/dev/null)
ARTIST=$(playerctl metadata artist 2>/dev/null)
ALBUM=$(playerctl metadata album 2>/dev/null)

if [ -z "$TITLE" ]; then
    notify-send "  Media" "No hay nada reproduciéndose"
    exit 1
fi

if [ -n "$ARTIST" ]; then
    INFO="$TITLE  •  $ARTIST"
else
    INFO="$TITLE"
fi

if [ "$STATUS" = "Playing" ]; then
    TOGGLE_ICON=""
    TOGGLE_LABEL="Pausa"
else
    TOGGLE_ICON=""
    TOGGLE_LABEL="Reproducir"
fi

ACTION=$(printf "%s %s\n  Anterior\n  Siguiente" "$TOGGLE_ICON" "$TOGGLE_LABEL" | rofi -dmenu -p "$INFO" -theme ~/.config/rofi/themes/media.rasi)

case "$ACTION" in
    *Pausa|*Reproducir) playerctl play-pause ;;
    *Anterior) playerctl previous ;;
    *Siguiente) playerctl next ;;
esac
