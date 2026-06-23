#!/bin/bash

entries=()

add_group() {
    entries+=("$1")
}

add_entry() {
    local keys="$1"
    local desc="$2"
    printf -v padded "%-30s" "$keys"
    entries+=("   $padded → $desc")
}

add_group "── Gestión de ventanas ──"
add_entry "SUPER + Q"              "Terminal (kitty)"
add_entry "SUPER + C"              "Cerrar ventana"
add_entry "SUPER + V"              "Toggle flotante"
add_entry "SUPER + P"              "Pseudo-tile"
add_entry "SUPER + J"              "Toggle split (dwindle)"
add_entry "SUPER + ←↑→↓"          "Mover foco"
add_entry "SUPER + click izq"      "Arrastrar ventana"
add_entry "SUPER + click der"      "Redimensionar ventana"

add_group "── Workspaces ──"
add_entry "SUPER + 0-9"            "Cambiar workspace"
add_entry "SUPER + SHIFT + 0-9"    "Mover ventana a workspace"
add_entry "SUPER + S"              "Toggle scratchpad (magic)"
add_entry "SUPER + SHIFT + S"      "Mover ventana a scratchpad"
add_entry "SUPER + scroll"         "Workspace anterior/siguiente"

add_group "── Multimedia ──"
add_entry "XF86AudioRaiseVolume"   "Subir volumen"
add_entry "XF86AudioLowerVolume"   "Bajar volumen"
add_entry "XF86AudioMute"          "Silenciar audio"
add_entry "XF86AudioMicMute"       "Silenciar micrófono"
add_entry "XF86AudioNext"          "Siguiente canción"
add_entry "XF86AudioPrev"          "Canción anterior"
add_entry "XF86AudioPlay/Pause"    "Play / Pausa"

add_group "── Brillo y pantalla ──"
add_entry "XF86MonBrightnessUp"    "Subir brillo pantalla"
add_entry "XF86MonBrightnessDown"  "Bajar brillo pantalla"
add_entry "XF86KbdBrightnessUp"    "Brillo teclado +"
add_entry "XF86KbdBrightnessDown"  "Brillo teclado -"
add_entry "SUPER + O"              "Apagar pantalla"

add_group "── Sistema ──"
add_entry "SUPER + X"              "Power menu (wlogout)"
add_entry "SUPER + R"              "Rofi (drun)"
add_entry "SUPER + E"              "Thunar (archivos)"
add_entry "SUPER + F1"             "Mostrar esta ayuda"
add_entry "SUPER + M"              "Cerrar sesión"
add_entry "SUPER + N"              "Toggle notificaciones"
add_entry "SUPER + B"              "Toggle Waybar"
add_entry "SUPER + A"              "nwgcc (controles)"
add_entry "SUPER + D"              "nwg-displays"
add_entry "SUPER + SHIFT + Space"  "Cambiar layout teclado"

add_group "── Capturas ──"
add_entry "SUPER + SHIFT + A"      "Capturar pantalla completa"
add_entry "SUPER + SHIFT + D"      "Capturar región"
add_entry "SUPER + SHIFT + W"      "Capturar ventana"

add_group "── Utilidades ──"
add_entry "SUPER + T"              "normcap (OCR)"
add_entry "SUPER + I"              "rofimoji (emojis)"
add_entry "SUPER + SHIFT + V"      "Cliphist (portapapeles)"

printf '%s\n' "${entries[@]}" | rofi -dmenu -i -p "Atajos" \
    -theme-str 'window {width: 45%;}' \
    -theme-str 'listview {lines: 14;}'
