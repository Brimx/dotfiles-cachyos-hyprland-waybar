# Dotfiles — CachyOS / Hyprland / Waybar

**ASUS Vivobook S14 Q423** · Core Ultra 5 226V · Arc 130V Xe2 · OLED WUXGA

## Structure

```
cachyos/
├── config.fish         # Fish shell
├── gtk/
│   └── settings.ini    # GTK theme
├── hyprland/           # Hyprland (window manager)
├── kitty/              # Kitty terminal
├── rofi/               # App launcher
├── waybar/             # Status bar
├── wlogout/            # Power menu
└── wofi/               # (future)
```

## Stack

| Component | Choice |
|-----------|--------|
| WM | Hyprland (Lua config) |
| Bar | Waybar (CSS + JSONC) |
| Launcher | Rofi |
| Terminal | Kitty |
| Shell | Fish |
| Notifications | Dunst |
| Power Menu | Wlogout |
| Lock | Hyprlock |
| Idle | Hypridle |
| Audio | PipeWire + pwvucontrol |
| Visual | Calf + EasyEffects |
| GPU | Xe2 (VA-API / Vulkan) |
