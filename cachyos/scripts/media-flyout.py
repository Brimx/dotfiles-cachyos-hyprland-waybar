#!/usr/bin/env python3
import gi
gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
from gi.repository import Gtk, Gdk, GLib, GdkPixbuf
import subprocess
import os
import signal
import sys
import threading

ICON_SIZE = 64
WIN_WIDTH = 380
WIN_HEIGHT = 100
PID_FILE = "/tmp/media-flyout.pid"

COLOR_BG = "rgba(20, 19, 17, 0.92)"
COLOR_FG = "#E3DFD7"
COLOR_ACCENT = "#337A96"
COLOR_MUTED = "rgba(227, 223, 215, 0.5)"

CSS = f"""
#flyout-box {{
    background: {COLOR_BG};
    border-radius: 16px;
    border: 1px solid rgba(227, 223, 215, 0.08);
}}
#title {{
    color: {COLOR_FG};
    font-weight: bold;
    font-size: 13px;
}}
#artist {{
    color: {COLOR_MUTED};
    font-size: 11px;
}}
button {{
    background: transparent;
    border: none;
    color: {COLOR_FG};
    font-size: 18px;
    padding: 6px 12px;
    border-radius: 8px;
}}
button:hover {{
    background: rgba(227, 223, 215, 0.08);
}}
button#play {{
    color: {COLOR_ACCENT};
    font-size: 22px;
}}
"""


class MediaFlyout:
    def __init__(self):
        self.win = Gtk.Window(type=Gtk.WindowType.POPUP)
        self.win.set_title("Media Flyout")
        self.win.set_default_size(WIN_WIDTH, WIN_HEIGHT)
        self.win.set_resizable(False)
        self.win.set_decorated(False)
        self.win.set_keep_above(True)
        self.win.set_skip_taskbar_hint(True)
        self.win.set_skip_pager_hint(True)
        self.win.set_position(Gtk.WindowPosition.NONE)
        self.win.set_accept_focus(False)
        self.win.set_focus_on_map(False)

        screen = self.win.get_screen()
        visual = screen.get_rgba_visual()
        if visual:
            self.win.set_visual(visual)

        provider = Gtk.CssProvider()
        provider.load_from_data(CSS.encode())
        Gtk.StyleContext.add_provider_for_screen(
            screen, provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        box.set_name("flyout-box")
        box.set_margin_top(8)
        box.set_margin_bottom(8)
        box.set_margin_start(12)
        box.set_margin_end(12)

        self.art = Gtk.Image()
        self.art.set_size_request(ICON_SIZE, ICON_SIZE)
        art_box = Gtk.EventBox()
        art_box.add(self.art)
        art_box.set_size_request(ICON_SIZE, ICON_SIZE)

        info_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        self.title_lbl = Gtk.Label(label="Sin reproducción")
        self.title_lbl.set_name("title")
        self.title_lbl.set_halign(Gtk.Align.START)
        self.title_lbl.set_ellipsize(True)
        self.title_lbl.set_max_width_chars(22)

        self.artist_lbl = Gtk.Label(label="")
        self.artist_lbl.set_name("artist")
        self.artist_lbl.set_halign(Gtk.Align.START)
        self.artist_lbl.set_ellipsize(True)
        self.artist_lbl.set_max_width_chars(22)

        info_box.pack_start(self.title_lbl, False, False, 0)
        info_box.pack_start(self.artist_lbl, False, False, 0)

        btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)
        self.prev_btn = Gtk.Button(label="")
        self.prev_btn.connect("clicked", self.on_prev)
        self.play_btn = Gtk.Button(label="")
        self.play_btn.set_name("play")
        self.play_btn.connect("clicked", self.on_play)
        self.next_btn = Gtk.Button(label="")
        self.next_btn.connect("clicked", self.on_next)

        btn_box.pack_start(self.prev_btn, False, False, 0)
        btn_box.pack_start(self.play_btn, False, False, 0)
        btn_box.pack_start(self.next_btn, False, False, 0)

        art_event = Gtk.EventBox()
        art_event.add(self.art)
        art_event.set_size_request(ICON_SIZE, ICON_SIZE)

        box.pack_start(art_event, False, False, 0)
        box.pack_start(info_box, True, True, 0)
        box.pack_start(btn_box, False, False, 0)

        self.win.add(box)
        self.win.connect("button-press-event", self.on_click_outside)
        self.win.connect("key-press-event", self.on_key)

        self.hide_timer = None
        GLib.timeout_add(1000, self.update_info)

        signal.signal(signal.SIGUSR1, lambda s, f: GLib.idle_add(self.toggle))
        GLib.unix_signal_add(GLib.PRIORITY_DEFAULT, signal.SIGUSR1, lambda: False)

    def center_top(self):
        display = Gdk.Display.get_default()
        if not display:
            return
        monitor = display.get_primary_monitor()
        if not monitor:
            monitor = display.get_monitor(0)
        gm = monitor.get_geometry()
        x = gm.x + (gm.width - WIN_WIDTH) // 2
        y = gm.y + 8
        self.win.move(x, y)

    def run_cmd(self, cmd):
        try:
            subprocess.run(cmd, capture_output=True, timeout=2)
        except Exception:
            pass

    def get_playerctl(self, *args):
        try:
            r = subprocess.run(["playerctl"] + list(args),
                               capture_output=True, text=True, timeout=2)
            return r.stdout.strip()
        except Exception:
            return ""

    def update_info(self):
        player = self.get_playerctl("-l").split("\n")[0] if self.get_playerctl("-l") else ""
        if not player:
            self.title_lbl.set_text("Sin reproducción")
            self.artist_lbl.set_text("")
            self.play_btn.set_label("")
            self.art.clear()
            return GLib.SOURCE_CONTINUE

        status = self.get_playerctl("status")
        title = self.get_playerctl("metadata", "title")
        artist = self.get_playerctl("metadata", "artist")
        art_url = self.get_playerctl("metadata", "mpris:artUrl")

        self.title_lbl.set_text(title[:35] if title else "Sin título")
        self.artist_lbl.set_text(artist[:35] if artist else "")
        self.play_btn.set_label("" if status == "Playing" else "")

        if art_url and art_url.startswith("file://"):
            path = art_url[7:]
            if os.path.exists(path):
                try:
                    pix = GdkPixbuf.Pixbuf.new_from_file_at_size(path, ICON_SIZE, ICON_SIZE)
                    self.art.set_from_pixbuf(pix)
                    return GLib.SOURCE_CONTINUE
                except Exception:
                    pass
        self.art.clear()
        return GLib.SOURCE_CONTINUE

    def on_play(self, _):
        self.run_cmd(["playerctl", "play-pause"])
        GLib.timeout_add(300, self.update_info)

    def on_prev(self, _):
        self.run_cmd(["playerctl", "previous"])
        GLib.timeout_add(300, self.update_info)

    def on_next(self, _):
        self.run_cmd(["playerctl", "next"])
        GLib.timeout_add(300, self.update_info)

    def on_click_outside(self, _, event):
        self.hide()

    def on_key(self, _, event):
        if event.keyval == Gdk.KEY_Escape:
            self.hide()

    def show(self):
        self.update_info()
        self.center_top()
        self.win.show_all()
        self.reset_timer()

    def hide(self):
        self.win.hide()
        if self.hide_timer:
            GLib.source_remove(self.hide_timer)
            self.hide_timer = None

    def toggle(self):
        if self.win.get_visible():
            self.hide()
        else:
            self.show()

    def reset_timer(self):
        if self.hide_timer:
            GLib.source_remove(self.hide_timer)
        self.hide_timer = GLib.timeout_add_seconds(5, self.hide)

    def run(self):
        with open(PID_FILE, "w") as f:
            f.write(str(os.getpid()))
        Gtk.main()


def toggle_daemon():
    if not os.path.exists(PID_FILE):
        print("Daemon not running, starting...")
        subprocess.Popen([sys.executable, __file__, "daemon"],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return
    with open(PID_FILE) as f:
        pid = int(f.read().strip())
    try:
        os.kill(pid, signal.SIGUSR1)
    except ProcessLookupError:
        os.remove(PID_FILE)
        subprocess.Popen([sys.executable, __file__, "daemon"],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "daemon":
        MediaFlyout().run()
    else:
        toggle_daemon()
