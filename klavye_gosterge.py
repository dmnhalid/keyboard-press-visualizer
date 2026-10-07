# -*- coding: utf-8 -*-
"""
Sistem geneli TAM BOY sanal klavye gostergesi (Turkce Q duzeni).

Hangi programda olursan ol, bastigin tus ekrandaki sanal klavyede yanar.
Yon tuslari, numpad, Insert/Home/PageUp kumesi ve PrtSc/ScrLk/Pause dahildir.

Calistirma:  python klavye_gosterge.py   (gerekiyorsa yonetici olarak)
Bagimlilik:  pip install keyboard
"""

import queue
import tkinter as tk

try:
    import keyboard
except ImportError:
    raise SystemExit(
        "'keyboard' kutuphanesi bulunamadi.\n"
        "Kur:  pip install keyboard"
    )

# ---------------------------------------------------------------------------
# Renkler
# ---------------------------------------------------------------------------
WIN_BG     = "#1e1e1e"
NORMAL_BG  = "#2b2b2b"
NORMAL_FG  = "#bdbdbd"
ACTIVE_BG  = "#4da3ff"
ACTIVE_FG  = "#ffffff"
BORDER     = "#3a3a3a"
FONT       = ("Segoe UI", 10, "bold")
KEY_H      = 2            # tus yuksekligi (satir)
DEFAULT_W  = 4            # varsayilan tus genisligi (karakter)

# ---------------------------------------------------------------------------
# Tus tanim yardimcilari.  Her tus bir eslesme yontemi tasir:
#   K(label, sc)   -> normal tus, (scan_code, is_keypad=False) ile eslesir
#   KP(label, sc)  -> numpad tusu, (scan_code, is_keypad=True) ile eslesir
#   N(label, name) -> isimle eslesir (ayrik/karisik kodlu ozel tuslar icin)
# Donen tuple: (label, matcher, is_keypad, by_name)
# ---------------------------------------------------------------------------
def K(label, sc):   return (label, sc, False, False)
def KP(label, sc):  return (label, sc, True, False)
def N(label, name): return (label, name, False, True)

# Ozel genislikler (etikete gore).
WIDTH_OVERRIDE = {
    "← Backspace": 12, "Tab": 6, "Caps": 7, "Enter": 9, "Shift": 9,
    "Space": 30, "Ctrl": 6, "Alt": 6, "Win": 5, "Menu": 5,
    "PrtSc": 6, "ScrLk": 6, "Pause": 6, "NumLk": 6,
}

# ---------------------------------------------------------------------------
# Ana blok (sol taraf) - Turkce Q duzeni, satir satir
# ---------------------------------------------------------------------------
MAIN_ROWS = [
    [K('"', 41), K("1", 2), K("2", 3), K("3", 4), K("4", 5), K("5", 6),
     K("6", 7), K("7", 8), K("8", 9), K("9", 10), K("0", 11), K("*", 12),
     K("-", 13), K("← Backspace", 14)],

    [K("Tab", 15), K("Q", 16), K("W", 17), K("E", 18), K("R", 19), K("T", 20),
     K("Y", 21), K("U", 22), K("I", 23), K("O", 24), K("P", 25),
     K("Ğ", 26), K("Ü", 27)],

    [K("Caps", 58), K("A", 30), K("S", 31), K("D", 32), K("F", 33), K("G", 34),
     K("H", 35), K("J", 36), K("K", 37), K("L", 38), K("Ş", 39),
     K("İ", 40), K(",", 43), K("Enter", 28)],

    [K("Shift", 42), K("<", 86), K("Z", 44), K("X", 45), K("C", 46), K("V", 47),
     K("B", 48), K("N", 49), K("M", 50), K("Ö", 51), K("Ç", 52),
     K(".", 53), K("Shift", 54)],

    [K("Ctrl", 29), K("Win", 91), K("Alt", 56), K("Space", 57), K("Alt", 56),
     K("Menu", 93), K("Ctrl", 29)],
]

# Fonksiyon sirasi (en ust)
FUNC_GROUPS = [
    [K("Esc", 1)],
    [K("F1", 59), K("F2", 60), K("F3", 61), K("F4", 62)],
    [K("F5", 63), K("F6", 64), K("F7", 65), K("F8", 66)],
    [K("F9", 67), K("F10", 68), K("F11", 87), K("F12", 88)],
    [N("PrtSc", "print screen"), N("ScrLk", "scroll lock"), N("Pause", "pause")],
]

# Navigasyon kumesi (Ins/Home/PgUp ...) ve yon tuslari - (satir, sutun)
NAV_GRID = [
    (0, 0, K("Ins", 82)), (0, 1, K("Home", 71)), (0, 2, K("PgUp", 73)),
    (1, 0, K("Del", 83)), (1, 1, K("End", 79)),  (1, 2, K("PgDn", 81)),
    # yon tuslari (ok tuslari)
    (3, 1, K("↑", 72)),
    (4, 0, K("←", 75)), (4, 1, K("↓", 80)), (4, 2, K("→", 77)),
]

# Numpad - (satir, sutun, columnspan, key)
NUMPAD_GRID = [
    (0, 0, 1, N("NumLk", "num lock")), (0, 1, 1, KP("/", 53)),
    (0, 2, 1, KP("*", 55)), (0, 3, 1, KP("-", 74)),
    (1, 0, 1, KP("7", 71)), (1, 1, 1, KP("8", 72)),
    (1, 2, 1, KP("9", 73)), (1, 3, 1, KP("+", 78)),
    (2, 0, 1, KP("4", 75)), (2, 1, 1, KP("5", 76)), (2, 2, 1, KP("6", 77)),
    (3, 0, 1, KP("1", 79)), (3, 1, 1, KP("2", 80)),
    (3, 2, 1, KP("3", 81)), (3, 3, 1, KP("↵", 28)),
    (4, 0, 2, KP("0", 82)), (4, 2, 1, KP(".", 83)),
]


class KlavyeGosterge:
    def __init__(self, root):
        self.root = root
        self.queue = queue.Queue()
        self.key_map = {}    # (scan_code, is_keypad) -> [Label, ...]
        self.name_map = {}   # name -> [Label, ...]

        root.title("Klavye Gostergesi - Turkce Q (Tam Boy)")
        root.configure(bg=WIN_BG)
        root.resizable(False, False)

        # --- Fonksiyon sirasi ---
        func_frame = tk.Frame(root, bg=WIN_BG)
        func_frame.pack(padx=8, pady=(8, 2), anchor="w")
        for i, group in enumerate(FUNC_GROUPS):
            if i > 0:
                tk.Frame(func_frame, width=18, bg=WIN_BG).pack(side="left")
            for spec in group:
                self._make(func_frame, spec).pack(side="left", padx=2)

        # --- Govde: ana blok | nav | numpad ---
        body = tk.Frame(root, bg=WIN_BG)
        body.pack(padx=8, pady=2, anchor="w")

        main_frame = tk.Frame(body, bg=WIN_BG)
        main_frame.pack(side="left", anchor="n")
        for row in MAIN_ROWS:
            rf = tk.Frame(main_frame, bg=WIN_BG)
            rf.pack(anchor="w", pady=2)
            for spec in row:
                self._make(rf, spec).pack(side="left", padx=2)

        nav_frame = tk.Frame(body, bg=WIN_BG)
        nav_frame.pack(side="left", anchor="n", padx=(16, 0))
        for r, c, spec in NAV_GRID:
            self._make(nav_frame, spec).grid(row=r, column=c, padx=2, pady=2)

        numpad_frame = tk.Frame(body, bg=WIN_BG)
        numpad_frame.pack(side="left", anchor="n", padx=(16, 0))
        for r, c, span, spec in NUMPAD_GRID:
            self._make(numpad_frame, spec).grid(
                row=r, column=c, columnspan=span, padx=2, pady=2, sticky="we"
            )

        info = tk.Label(
            root,
            text="Her yerde bastigin tus burada yanar. Kapatmak icin pencereyi kapat.",
            bg=WIN_BG, fg="#777777", font=("Segoe UI", 8),
        )
        info.pack(pady=(4, 8))

        keyboard.hook(self._on_key_event)
        root.protocol("WM_DELETE_WINDOW", self._on_close)
        self._poll_queue()

    def _make(self, parent, spec):
        """spec'ten Label olusturur ve eslesme haritalarina kaydeder."""
        label, matcher, is_keypad, by_name = spec
        width = WIDTH_OVERRIDE.get(label, DEFAULT_W)
        lbl = tk.Label(
            parent, text=label, width=width, height=KEY_H,
            bg=NORMAL_BG, fg=NORMAL_FG, font=FONT,
            relief="flat", bd=0,
            highlightbackground=BORDER, highlightthickness=1,
        )
        if by_name:
            self.name_map.setdefault(matcher, []).append(lbl)
        else:
            self.key_map.setdefault((matcher, is_keypad), []).append(lbl)
        return lbl

    def _on_key_event(self, event):
        # keyboard'in thread'inde calisir -> sadece kuyruga yaz.
        self.queue.put((event.scan_code, event.is_keypad, event.name,
                        event.event_type))

    def _poll_queue(self):
        try:
            while True:
                sc, is_keypad, name, event_type = self.queue.get_nowait()
                widgets = self.key_map.get((sc, is_keypad), [])
                if name:
                    widgets = widgets + self.name_map.get(name, [])
                for widget in widgets:
                    if event_type == keyboard.KEY_DOWN:
                        widget.config(bg=ACTIVE_BG, fg=ACTIVE_FG)
                    else:
                        widget.config(bg=NORMAL_BG, fg=NORMAL_FG)
        except queue.Empty:
            pass
        self.root.after(15, self._poll_queue)

    def _on_close(self):
        try:
            keyboard.unhook_all()
        except Exception:
            pass
        self.root.destroy()


def main():
    root = tk.Tk()
    KlavyeGosterge(root)
    root.mainloop()


if __name__ == "__main__":
    main()
