#!/usr/bin/env python3
"""Hand-built wireframes for the HomeSteadyLink web app (USB / WebUSB) PRD.
Every element comes from the GATT contract (firmware spec/gatt.md) and the
Android app flow (mobile-app screens S1-S6). No element is invented.
Desktop browser frames, 1280x800. Run: python3 build-web-wireframes.py ;
renders via cdp-shot.js (node cdp-shot.js file://$PWD/<name>.svg $PWD/<name>.png 1280 800).

No setup code anywhere in this flow (Den, 2026-11-15): physical USB
presence is the trust root — the cable is the credential. The setup
code stays for BLE only.
"""
import os
from xml.sax.saxutils import escape

OUT = os.path.dirname(os.path.abspath(__file__))
TEAL = "#0F766E"
DARK = "#111827"
GRAY = "#6B7280"
LINE = "#E5E7EB"
GREEN = "#15803D"
GREEN_BG = "#DCFCE7"
RED = "#DC2626"
RED_BG = "#FEE2E2"
AMBER = "#B45309"
AMBER_BG = "#FEF3C7"
SLATE = "#475569"
PAGE_BG = "#F9FAFB"
URL = "https://homesteadlink.github.io/web-app/"

def esc(s):
    return escape(str(s))

def t(s, x, y, size=14, fill=DARK, weight="normal", anchor="start", style=""):
    st = f' font-style="{style}"' if style else ""
    return (f'<text x="{x}" y="{y}" font-family="Arial, Helvetica, sans-serif" '
            f'font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}"{st}>{esc(s)}</text>')

def mono(x, y, s, size=12, fill=DARK, anchor="start"):
    return (f'<text x="{x}" y="{y}" font-family="monospace" font-size="{size}" '
            f'fill="{fill}" text-anchor="{anchor}">{esc(s)}</text>')

def rect(x, y, w, h, fill="#FFFFFF", stroke=LINE, sw=1, rx=12):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'

def line(x1, y1, x2, y2, stroke=LINE, sw=1, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{sw}"{d}/>'

def circle(cx, cy, r, fill, stroke="none", sw=0):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'

def path(d, fill="none", stroke=DARK, sw=1.5):
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/>'

# ---- tiny icons (24x24 box at x,y), same palette as the mobile wireframes ----
def ic_router(x, y, c=TEAL):
    return (f'<g stroke="{c}" stroke-width="2" fill="none" stroke-linecap="round">'
            f'<rect x="{x+3}" y="{y+12}" width="18" height="8" rx="2" fill="{c}" stroke="none"/>'
            f'<line x1="{x+8}" y1="{y+12}" x2="{x+8}" y2="{y+5}"/><line x1="{x+16}" y1="{y+12}" x2="{x+16}" y2="{y+5}"/>'
            f'<circle cx="{x+8}" cy="{y+4}" r="1.6" fill="{c}" stroke="none"/><circle cx="{x+16}" cy="{y+4}" r="1.6" fill="{c}" stroke="none"/>'
            f'<circle cx="{x+9}" cy="{y+16}" r="1.3" fill="#fff" stroke="none"/><circle cx="{x+15}" cy="{y+16}" r="1.3" fill="#fff" stroke="none"/></g>')

def ic_wifi(x, y, c=TEAL):
    return (f'<g stroke="{c}" stroke-width="2" fill="none" stroke-linecap="round">'
            f'<path d="M{x+3} {y+9} Q{x+12} {y+1} {x+21} {y+9}"/>'
            f'<path d="M{x+6} {y+13} Q{x+12} {y+7} {x+18} {y+13}"/>'
            f'<circle cx="{x+12}" cy="{y+17}" r="1.8" fill="{c}" stroke="none"/></g>')

def ic_shield(x, y, c=TEAL):
    return (f'<g stroke="{c}" stroke-width="2" fill="none" stroke-linejoin="round">'
            f'<path d="M{x+12} {y+2} L{x+20} {y+5} V{y+11} Q{x+20} {y+19} {x+12} {y+22} Q{x+4} {y+19} {x+4} {y+11} V{y+5} Z"/>'
            f'<path d="M{x+8.5} {y+11} L{x+11} {y+13.5} L{x+16} {y+8}"/></g>')

def ic_lock(x, y, c=GREEN):
    return (f'<g stroke="{c}" stroke-width="2" fill="none">'
            f'<rect x="{x+5}" y="{y+10}" width="14" height="10" rx="2" fill="{c}" stroke="none"/>'
            f'<path d="M{x+8} {y+10} V{y+7} a4 4 0 0 1 8 0 V{y+10}"/></g>')

def ic_check(x, y, c=GREEN):
    return (f'<g><circle cx="{x+12}" cy="{y+12}" r="10" fill="{c}"/>'
            f'<path d="M{x+7} {y+12} L{x+11} {y+16} L{x+17} {y+8}" stroke="#fff" stroke-width="2.2" fill="none" stroke-linecap="round"/></g>')

def ic_error(x, y, c=RED):
    return (f'<g><circle cx="{x+12}" cy="{y+12}" r="10" fill="{c}"/>'
            f'<path d="M{x+12} {y+7} V{y+13}" stroke="#fff" stroke-width="2.4" stroke-linecap="round"/>'
            f'<circle cx="{x+12}" cy="{y+17}" r="1.4" fill="#fff"/></g>')

def ic_eye(x, y, c=GRAY):
    return (f'<g stroke="{c}" stroke-width="1.8" fill="none">'
            f'<path d="M{x+2} {y+12} Q{x+12} {y+3} {x+22} {y+12} Q{x+12} {y+21} {x+2} {y+12} Z"/>'
            f'<circle cx="{x+12}" cy="{y+12}" r="3.2"/></g>')

def ic_key(x, y, c=GRAY):
    return (f'<g stroke="{c}" stroke-width="2" fill="none" stroke-linecap="round">'
            f'<circle cx="{x+8}" cy="{y+9}" r="4.5"/><path d="M{x+11.5} {y+12.5} L{x+19} {y+20} M{x+16} {y+17} L{x+19} {y+14}"/></g>')

def ic_usb(x, y, c=TEAL):
    # USB trident-ish glyph: plug body + prongs
    return (f'<g stroke="{c}" stroke-width="2" fill="none" stroke-linecap="round">'
            f'<rect x="{x+8}" y="{y+10}" width="8" height="12" rx="2"/>'
            f'<line x1="{x+10}" y1="{y+10}" x2="{x+10}" y2="{y+4}"/><line x1="{x+14}" y1="{y+10}" x2="{x+14}" y2="{y+4}"/>'
            f'<circle cx="{x+10}" cy="{y+3}" r="1.4" fill="{c}" stroke="none"/><circle cx="{x+14}" cy="{y+3}" r="1.4" fill="{c}" stroke="none"/></g>')

def ic_vpnlock(x, y, c="#FFFFFF"):
    return (f'<g stroke="{c}" stroke-width="1.8" fill="none" stroke-linecap="round">'
            f'<circle cx="{x+10}" cy="{y+12}" r="7"/><path d="M{x+3} {y+12} H{x+17} M{x+10} {y+5} Q{x+13} {y+12} {x+10} {y+19} Q{x+7} {y+12} {x+10} {y+5}"/>'
            f'<rect x="{x+15}" y="{y+14}" width="7" height="6" rx="1" fill="{c}" stroke="none"/>'
            f'<path d="M{x+16.5} {y+14} V{y+12.5} a2 2 0 0 1 4 0 V{y+14}"/></g>')

# ---- desktop browser chrome + page scaffold ----
# Content column: x 280..1000 (720 wide). Page area y 76..800.
CX, CW = 280, 720
CX1 = CX + CW

def browser_open(title):
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="800" viewBox="0 0 1280 800">',
         f'<rect x="0" y="0" width="1280" height="800" fill="#FFFFFF"/>',
         f'<rect x="0" y="0" width="1280" height="800" fill="none" stroke="#9CA3AF" stroke-width="1.5"/>',
         # tab bar
         f'<rect x="0" y="0" width="1280" height="36" fill="#E5E7EB"/>',
         f'<circle cx="16" cy="18" r="6" fill="#FCA5A5"/><circle cx="36" cy="18" r="6" fill="#FDE68A"/><circle cx="56" cy="18" r="6" fill="#86EFAC"/>',
         f'<rect x="76" y="6" width="220" height="26" rx="8" fill="#FFFFFF"/>',
         t("HomeSteadyLink — Setup", 88, 24, 12, DARK, "bold"),
         t("×", 284, 24, 12, GRAY, "bold"),
         # address bar
         f'<rect x="0" y="36" width="1280" height="40" fill="#F3F4F6"/>',
         f'<rect x="76" y="44" width="620" height="26" rx="13" fill="#FFFFFF" stroke="{LINE}"/>',
         ic_lock(86, 47, GREEN),
         t(URL, 112, 62, 12, DARK),
         t("WebUSB", 712, 62, 12, TEAL, "bold"),
         t(title, 1120, 18, 11, GRAY, "normal", "end"),
         f'<rect x="0" y="76" width="1280" height="724" fill="{PAGE_BG}"/>']
    return p

def browser_close(parts):
    parts.append('</svg>')
    return "\n".join(parts)

def page_header(parts, step, title, sub):
    """Page header inside the content column. Returns y below the header."""
    y = 100
    parts.append(ic_router(CX, y))
    parts.append(t("HomeSteadyLink", CX + 32, y + 17, 20, DARK, "bold"))
    parts.append(t(step, CX1, y + 17, 13, GRAY, "normal", "end"))
    y += 36
    parts.append(t(title, CX, y + 22, 24, DARK, "bold"))
    y += 30
    parts.append(t(sub, CX, y + 16, 14, GRAY))
    y += 28
    return y

def card(parts, x, y, w, h):
    parts.append(rect(x, y, w, h, fill="#FFFFFF", stroke=LINE, rx=12))
    return y

def btn(parts, x, y, w, h, label, kind="primary"):
    if kind == "primary":
        parts.append(rect(x, y, w, h, fill=TEAL, stroke=TEAL, rx=24))
        parts.append(t(label, x + w / 2, y + h / 2 + 5, 15, "#FFFFFF", "bold", "middle"))
    elif kind == "outline":
        parts.append(rect(x, y, w, h, fill="#FFFFFF", stroke=TEAL, rx=24))
        parts.append(t(label, x + w / 2, y + h / 2 + 5, 15, TEAL, "bold", "middle"))
    elif kind == "ghost":
        parts.append(rect(x, y, w, h, fill="#FFFFFF", stroke=LINE, rx=24))
        parts.append(t(label, x + w / 2, y + h / 2 + 5, 15, DARK, "bold", "middle"))
    elif kind == "danger-outline":
        parts.append(rect(x, y, w, h, fill="#FFFFFF", stroke=RED, rx=24))
        parts.append(t(label, x + w / 2, y + h / 2 + 5, 15, RED, "bold", "middle"))
    return y + h

def annot(parts, y, s):
    parts.append(t(s, CX, y + 11, 11, GRAY, "normal", "start", "italic"))
    return y + 16

def sect(parts, y, s):
    parts.append(t(s, CX, y + 15, 15, DARK, "bold"))
    return y + 24

def field(parts, x, y, w, label, value, masked=False, hint=None):
    parts.append(t(label, x, y + 14, 12, GRAY))
    y += 18
    parts.append(rect(x, y, w, 46, fill="#FFFFFF", stroke="#9CA3AF", rx=8))
    parts.append(t(value, x + 12, y + 30, 15, DARK))
    y += 46
    if hint:
        parts.append(t(hint, x, y + 14, 11, GRAY, "normal", "start", "italic"))
        y += 18
    return y

def step_row(parts, x, y, w, num, label, state):
    """One row of the progress tracker. state: done|active|waiting|failed."""
    if state == "done":
        parts.append(circle(x + 12, y + 12, 10, GREEN))
        parts.append(path(f"M{x+7} {y+12} L{x+11} {y+16} L{x+17} {y+8}", fill="none", stroke="#FFFFFF", sw=2))
        parts.append(t(label, x + 30, y + 16, 14, DARK))
        parts.append(t("Done", x + w, y + 16, 13, GREEN, "bold", "end"))
    elif state == "active":
        parts.append(circle(x + 12, y + 12, 11, "#FFFFFF", TEAL, 2))
        parts.append(path(f"M{x+12} {y+1} A11 11 0 0 1 {x+23} {y+12}", fill="none", stroke=TEAL, sw=2.5))
        parts.append(t(label, x + 30, y + 16, 14, DARK, "bold"))
        parts.append(t("In progress…", x + w, y + 16, 13, TEAL, "bold", "end"))
    elif state == "failed":
        parts.append(circle(x + 12, y + 12, 10, RED))
        parts.append(t("✕", x + 12, y + 16, 11, "#FFFFFF", "bold", "middle"))
        parts.append(t(label, x + 30, y + 16, 14, DARK, "bold"))
        parts.append(t("Failed", x + w, y + 16, 13, RED, "bold", "end"))
    else:
        parts.append(circle(x + 12, y + 12, 10, "#FFFFFF", "#9CA3AF", 1.5))
        parts.append(t(label, x + 30, y + 16, 14, GRAY))
        parts.append(t("Waiting", x + w, y + 16, 13, GRAY, "bold", "end"))
    return y + 30

# ================= flow-web — user flow =================
def frame_flow():
    p = browser_open("W-flow — Web app flow")
    y = 100
    p.append(t("Web app flow", CX, y + 22, 24, DARK, "bold"))
    y += 34
    p.append(t("Connect over USB → Wi-Fi → VPN → Progress → Device. One decision per step.", CX, y + 16, 14, GRAY))
    y += 40
    nodes = [
        ("W1 · Connect", "pick the router over USB"),
        ("W2 · Wi-Fi", "networks near the router"),
        ("W3 · VPN", "WireGuard / Tailscale / Skip"),
        ("W4 · Progress", "live provisioning"),
        ("W5 · Device", "steady-state control"),
    ]
    NX, NW, NH, GAP = CX, 200, 52, 24
    yy = y
    centers = []
    for idx, (title, sub) in enumerate(nodes):
        p.append(rect(NX, yy, NW, NH, fill="#FFFFFF", stroke=TEAL, rx=10))
        p.append(t(title, NX + 12, yy + 21, 14, DARK, "bold"))
        p.append(t(sub, NX + 12, yy + 39, 11, GRAY))
        centers.append(yy + NH / 2)
        if idx < len(nodes) - 1:
            ax = NX + NW / 2
            p.append(line(ax, yy + NH, ax, yy + NH + GAP, stroke=TEAL, sw=2))
            p.append(path(f"M{ax-5} {yy+NH+GAP-6} L{ax} {yy+NH+GAP} L{ax+5} {yy+NH+GAP-6}", fill="none", stroke=TEAL, sw=2))
        yy += NH + GAP
    BX, BW = CX + 250, 470
    def branch(by, bh, lines, from_y, elbow=None):
        p.append(rect(BX, by, BW, bh, fill="#FFFBEB", stroke="#F59E0B", rx=10))
        ly = by + 20
        for ln in lines:
            p.append(t(ln, BX + 12, ly, 13, DARK))
            ly += 18
        if elbow is None:
            p.append(line(NX + NW, from_y, BX, from_y, stroke="#F59E0B", sw=1.5, dash="4 3"))
            p.append(path(f"M{BX-6} {from_y-4} L{BX} {from_y} L{BX-6} {from_y+4}", fill="none", stroke="#F59E0B", sw=1.5))
        else:
            ex, ey = elbow
            p.append(line(NX + NW, from_y, ex, from_y, stroke="#F59E0B", sw=1.5, dash="4 3"))
            p.append(line(ex, from_y, ex, ey, stroke="#F59E0B", sw=1.5, dash="4 3"))
            p.append(line(ex, ey, BX, ey, stroke="#F59E0B", sw=1.5, dash="4 3"))
            p.append(path(f"M{BX-6} {ey-4} L{BX} {ey} L{BX-6} {ey+4}", fill="none", stroke="#F59E0B", sw=1.5))
    prog_cy = centers[3]
    dev_cy = centers[4]
    branch(178, 44, ["No device / permission denied → back to Connect"], centers[0])
    branch(254, 44, ["No networks found → scan again on Wi-Fi"], centers[1])
    branch(406, 64, ["Wi-Fi auth failed → back to Wi-Fi", "Captive portal → portal pass → re-check"], prog_cy)
    branch(478, 46, ["VPN failed → Retry VPN / continue without VPN"], prog_cy, elbow=(CX + 225, 501))
    branch(536, 46, ["Factory Reset / Disconnect → Connect"], dev_cy, elbow=(CX + 225, 559))
    ny = 604
    p.append(line(CX, ny, CX1, ny))
    ny += 24
    for ln in ["Browser picker: the device list is the browser's own dialog — the page cannot draw it.",
              "Back button: browser back returns to the previous step; Disconnect returns to Connect.",
              "No setup code: the USB cable is the trust — anyone holding the board and a cable can control it."]:
        p.append(t(ln, CX, ny, 13, GRAY))
        ny += 20
    return browser_close(p)

# ================= W1 — Connect =================
def frame_w1():
    p = browser_open("W1 — Connect")
    y = page_header(p, "Step 1 of 4 · Connect", "Connect your router",
                    "Plug the router into this computer with a USB cable, then choose it below.")
    # hero card
    h = 150
    card(p, CX, y, CW, h)
    p.append(ic_usb(CX + 24, y + 22, TEAL))
    p.append(t("Your router is a USB device", CX + 64, y + 36, 17, DARK, "bold"))
    p.append(t("The page talks to it over USB — no Bluetooth, no Wi-Fi needed for setup.", CX + 64, y + 60, 13, GRAY))
    p.append(t("The router shows up as “HomeSteadyLink” in the browser's device list.", CX + 64, y + 80, 13, GRAY))
    p.append(rect(CX + 24, y + 100, 220, 34, fill="#EFF6F6", stroke=TEAL, rx=17))
    p.append(t("✓  USB cable connected", CX + 134, y + 121, 13, TEAL, "bold", "middle"))
    y += h + 16
    y = btn(p, CX, y, 260, 52, "Connect router", "primary")
    y += 14
    y = annot(p, y, "Opens the browser's device picker. Pick “HomeSteadyLink” → Wi-Fi.")
    y += 8
    # browser note card
    h = 96
    card(p, CX, y, CW, h)
    p.append(t("Which browsers work", CX + 24, y + 28, 14, DARK, "bold"))
    p.append(t("Chrome and Edge on macOS, Windows, and Linux. Android Chrome works with a USB cable.", CX + 24, y + 52, 13, GRAY))
    p.append(t("Safari can't use USB — use the router's Wi-Fi setup page instead (see below).", CX + 24, y + 74, 13, GRAY))
    y += h + 12
    p.append(t("No USB? Open the router's Wi-Fi setup page: join the “HomeSteady-…” network, then open", CX, y + 14, 12, GRAY))
    p.append(t("http://192.168.65.1:8080", CX, y + 32, 12, TEAL, "bold"))
    return browser_close(p)

# ================= W1-unsupported — browser without WebUSB =================
def frame_w1_unsupported():
    p = browser_open("W1 — Browser not supported")
    y = page_header(p, "Step 1 of 4 · Connect", "Connect your router",
                    "Plug the router into this computer with a USB cable, then choose it below.")
    h = 190
    card(p, CX, y, CW, h)
    p.append(ic_error(CX + 24, y + 22, RED))
    p.append(t("Your browser can't use USB", CX + 64, y + 36, 17, DARK, "bold"))
    p.append(t("This page needs WebUSB, which Safari and Firefox don't support.", CX + 64, y + 60, 13, GRAY))
    p.append(t("Use Chrome or Edge on macOS, Windows, or Linux — or Android Chrome.", CX + 64, y + 80, 13, GRAY))
    p.append(line(CX + 24, y + 100, CX1 - 24, y + 100))
    p.append(t("What to do next", CX + 24, y + 124, 13, DARK, "bold"))
    p.append(t("1. Open this page in Chrome or Edge.  2. Or use the router's Wi-Fi setup page (below).", CX + 24, y + 146, 13, GRAY))
    p.append(rect(CX + 24, y + 158, 300, 24, fill="#F3F4F6", stroke=LINE, rx=6))
    p.append(t("Copy error details", CX + 174, y + 174, 12, DARK, "bold", "middle"))
    y += h + 16
    y = btn(p, CX, y, 260, 52, "Try again", "primary")
    y += 14
    p.append(t("No USB? Join the “HomeSteady-…” Wi-Fi network, then open http://192.168.65.1:8080", CX, y + 14, 12, GRAY))
    return browser_close(p)

# ================= W1-denied — permission denied / no device =================
def frame_w1_denied():
    p = browser_open("W1 — No router found")
    y = page_header(p, "Step 1 of 4 · Connect", "Connect your router",
                    "Plug the router into this computer with a USB cable, then choose it below.")
    h = 210
    card(p, CX, y, CW, h)
    p.append(ic_error(CX + 24, y + 22, RED))
    p.append(t("No router found", CX + 64, y + 36, 17, DARK, "bold"))
    p.append(t("The browser couldn't access the router over USB.", CX + 64, y + 60, 13, GRAY))
    p.append(line(CX + 24, y + 78, CX1 - 24, y + 78))
    p.append(t("Check this", CX + 24, y + 102, 13, DARK, "bold"))
    p.append(t("• The USB cable is plugged into the router and this computer.", CX + 24, y + 124, 13, GRAY))
    p.append(t("• You picked “HomeSteadyLink” in the device list — cancelling returns here.", CX + 24, y + 144, 13, GRAY))
    p.append(t("• The browser has USB permission (lock icon → Site settings → USB).", CX + 24, y + 164, 13, GRAY))
    p.append(rect(CX + 24, y + 178, 300, 24, fill="#F3F4F6", stroke=LINE, rx=6))
    p.append(t("Copy error details", CX + 174, y + 194, 12, DARK, "bold", "middle"))
    y += h + 16
    y = btn(p, CX, y, 260, 52, "Try again", "primary")
    y += 14
    y = annot(p, y, "Full error (technical detail) lives behind “Copy error details”: the USB error name")
    y = annot(p, y, "and the browser's reason, copied as one block for a bug report.")
    return browser_close(p)

# ================= W2 — Wi-Fi =================
def frame_w2():
    p = browser_open("W2 — Wi-Fi")
    y = page_header(p, "Step 2 of 4 · Wi-Fi", "Connect the router to Wi-Fi",
                    "These are the networks the router can see from where it sits.")
    # network list
    y = sect(p, y, "Networks near the router (3)")
    p.append(t("Scan again", CX1, y - 9, 12, TEAL, "bold", "end"))
    nets = [("HomeNet-5G", "−52 dBm · 5 GHz · Secured", True),
            ("Hotel_Guest", "−67 dBm · 2.4 GHz · Open", False),
            ("CoffeeShop", "−74 dBm · 5 GHz · Secured", False)]
    for ssid, meta, sel in nets:
        h = 58
        fill = "#EFF6F6" if sel else "#FFFFFF"
        stroke = TEAL if sel else LINE
        p.append(rect(CX, y, CW, h, fill=fill, stroke=stroke, rx=10))
        p.append(ic_wifi(CX + 16, y + 16, TEAL if sel else GRAY))
        p.append(t(ssid, CX + 52, y + 24, 15, DARK, "bold"))
        p.append(t(meta, CX + 52, y + 44, 12, GRAY))
        if sel:
            p.append(ic_check(CX1 - 40, y + 16, GREEN))
        y += h + 8
    y += 4
    # password field
    y = field(p, CX, y, CW, "Wi-Fi password for HomeNet-5G", "••••••••••")
    p.append(rect(CX, y + 2, 18, 18, fill="#FFFFFF", stroke="#9CA3AF", rx=4))
    p.append(t("Open network (no password)", CX + 26, y + 16, 14, DARK))
    y += 30
    # advanced
    p.append(t("Advanced", CX, y + 16, 14, DARK, "bold"))
    p.append(t("Show", CX1, y + 16, 13, TEAL, "bold", "end"))
    y += 26
    p.append(rect(CX, y + 2, 18, 18, fill="#FFFFFF", stroke="#9CA3AF", rx=4))
    p.append(t("Hidden network (type the name — it isn't broadcast)", CX + 26, y + 16, 13, DARK))
    y += 28
    p.append(t("Country", CX, y + 14, 12, GRAY))
    p.append(rect(CX, y + 18, 90, 40, fill="#FFFFFF", stroke="#9CA3AF", rx=8))
    p.append(t("US", CX + 12, y + 44, 14, DARK))
    p.append(t("Prefilled from this computer's locale — almost nobody changes it.", CX + 104, y + 44, 12, GRAY, "normal", "start", "italic"))
    y += 58 + 6
    y = btn(p, CX, y, 260, 52, "Connect to Wi-Fi", "primary")
    y += 12
    y = annot(p, y, "Nothing is written to the router yet — Connect sends Wi-Fi + VPN together on the next step.")
    return browser_close(p)

# ================= W2-wifi-empty — no networks found =================
def frame_w2_empty():
    p = browser_open("W2 — No networks found")
    y = page_header(p, "Step 2 of 4 · Wi-Fi", "Connect the router to Wi-Fi",
                    "These are the networks the router can see from where it sits.")
    y = sect(p, y, "Networks near the router (0)")
    p.append(t("Scan again", CX1, y - 9, 12, TEAL, "bold", "end"))
    h = 150
    card(p, CX, y, CW, h)
    p.append(ic_wifi(CX + 24, y + 22, GRAY))
    p.append(t("No networks found", CX + 64, y + 36, 16, DARK, "bold"))
    p.append(t("The router couldn't see any Wi-Fi networks from where it sits.", CX + 64, y + 60, 13, GRAY))
    p.append(t("Move the router closer to a Wi-Fi network, then scan again.", CX + 64, y + 80, 13, GRAY))
    p.append(rect(CX + 24, y + 104, 300, 24, fill="#F3F4F6", stroke=LINE, rx=6))
    p.append(t("Copy error details", CX + 174, y + 120, 12, DARK, "bold", "middle"))
    y += h + 16
    y = btn(p, CX, y, 200, 52, "Scan again", "primary")
    y += 12
    y = btn(p, CX, y, 260, 52, "Type a network name instead", "outline")
    y += 14
    y = annot(p, y, "Typing a name works for hidden networks too — the router scans for that name directly.")
    return browser_close(p)

# ================= W3 — VPN =================
def frame_w3():
    p = browser_open("W3 — VPN")
    y = page_header(p, "Step 3 of 4 · VPN", "Set up the VPN",
                    "The router routes all its traffic through the VPN, behind a kill switch.")
    # WireGuard card (default visible path)
    h = 170
    card(p, CX, y, CW, h)
    p.append(ic_shield(CX + 24, y + 20, TEAL))
    p.append(t("WireGuard", CX + 64, y + 32, 16, DARK, "bold"))
    p.append(t("Paste your WireGuard config (.conf file contents)", CX + 64, y + 54, 12, GRAY))
    p.append(rect(CX + 24, y + 68, CW - 48, 62, fill="#F9FAFB", stroke="#9CA3AF", rx=8))
    for i in range(3):
        p.append(mono(CX + 36, y + 88 + i * 18, "•" * 32, 13, DARK))
    p.append(ic_eye(CX1 - 60, y + 76, GRAY))
    p.append(rect(CX + 24, y + 140, 130, 24, fill="#FFFFFF", stroke=LINE, rx=6))
    p.append(t("Upload .conf file", CX + 89, y + 156, 12, DARK, "bold", "middle"))
    y += h + 12
    # Tailscale card
    h = 150
    card(p, CX, y, CW, h)
    p.append(ic_shield(CX + 24, y + 20, TEAL))
    p.append(t("Tailscale", CX + 64, y + 32, 16, DARK, "bold"))
    p.append(t("Join your tailnet — the router appears as a device on it.", CX + 64, y + 54, 12, GRAY))
    p.append(rect(CX + 24, y + 68, CW - 48, 34, fill="#FFFFFF", stroke="#9CA3AF", rx=8))
    p.append(ic_key(CX + 34, y + 76, GRAY))
    p.append(t("Auth key (tskey-auth-…)", CX + 62, y + 89, 13, GRAY))
    p.append(rect(CX + 24, y + 110, CW - 48, 34, fill="#FFFFFF", stroke="#9CA3AF", rx=8))
    p.append(t("Exit node (optional) — e.g. mullvad-us12", CX + 36, y + 131, 13, GRAY))
    y += h + 6
    y = annot(p, y, "Generate a key in your Tailscale admin console under Settings → Keys.")
    y += 4
    y = btn(p, CX, y, 260, 52, "Save & provision", "primary")
    y += 10
    y = btn(p, CX, y, 280, 46, "Skip VPN (Wi-Fi only)", "ghost")
    y += 10
    y = annot(p, y, "Save sends Wi-Fi + VPN together → Progress. Skip sends Wi-Fi only.")
    y = annot(p, y, "WireGuard or Tailscale — pick one. The other card stays empty.")
    return browser_close(p)

# ================= W4 — Progress =================
def frame_w4():
    p = browser_open("W4 — Progress")
    y = page_header(p, "Step 4 of 4 · Progress", "Setting up your router",
                    "Live status while the router joins Wi-Fi and starts the VPN.")
    # status card
    h = 76
    card(p, CX, y, CW, h)
    p.append(ic_wifi(CX + 24, y + 26, TEAL))
    p.append(t("Joining HomeNet-5G…", CX + 64, y + 34, 16, DARK, "bold"))
    p.append(t("Uplink SSID: HomeNet-5G", CX + 64, y + 58, 12, GRAY))
    y += h + 16
    # pipeline tracker
    y = sect(p, y, "Setup steps")
    steps = [("USB link", "done"),
             ("Joining Wi-Fi", "active"),
             ("Internet check", "waiting"),
             ("Starting VPN", "waiting")]
    for label, state in steps:
        y = step_row(p, CX, y, CW, "", label, state)
    y += 10
    y = annot(p, y, "The page polls the router over USB — every step updates live. No refresh needed.")
    y += 6
    y = btn(p, CX, y, 280, 52, "Back to Wi-Fi setup", "ghost")
    y += 12
    y = annot(p, y, "“Open device dashboard” replaces it once the router is online.")
    return browser_close(p)

# ================= W4-error — Wi-Fi auth failed =================
def frame_w4_error():
    p = browser_open("W4 — Wi-Fi failed")
    y = page_header(p, "Step 4 of 4 · Progress", "Setting up your router",
                    "Live status while the router joins Wi-Fi and starts the VPN.")
    # error card (full error per the rule: summary + detail + next action + copy)
    h = 250
    card(p, CX, y, CW, h)
    p.append(ic_error(CX + 24, y + 22, RED))
    p.append(t("The router couldn't join HomeNet-5G", CX + 64, y + 36, 17, DARK, "bold"))
    p.append(t("Check the password and try again.", CX + 64, y + 60, 13, GRAY))
    p.append(line(CX + 24, y + 78, CX1 - 24, y + 78))
    p.append(mono(CX + 24, y + 100, "error: wifi_auth_failed · state: wifi_auth_failed", 12, RED))
    p.append(mono(CX + 24, y + 120, "ssid: HomeNet-5G · bssid: aa:bb:cc:dd:ee:ff · rssi: -52", 12, GRAY))
    p.append(mono(CX + 24, y + 140, "router: HomeSteady-TR-8821 · fw 1.0.0 · usb: connected", 12, GRAY))
    p.append(t("What to do next: re-enter the Wi-Fi password. The old config still works if one was saved.", CX + 24, y + 168, 13, GRAY))
    p.append(rect(CX + 24, y + 186, 300, 24, fill="#F3F4F6", stroke=LINE, rx=6))
    p.append(t("Copy error details", CX + 174, y + 202, 12, DARK, "bold", "middle"))
    y += h + 16
    y = btn(p, CX, y, 300, 52, "Re-enter Wi-Fi password", "primary")
    y += 12
    y = annot(p, y, "Other errors use this same card: captive portal, VPN failed, no internet.")
    y = annot(p, y, "Each shows the plain-language summary first, the code small — never the code alone.")
    return browser_close(p)

# ================= W5 — Device dashboard =================
def frame_w5():
    p = browser_open("W5 — Device")
    y = page_header(p, "Device", "HomeSteady Travel Router", "Steady-state control of a provisioned router.")
    # status card
    h = 96
    card(p, CX, y, CW, h)
    p.append(ic_router(CX + 24, y + 22, TEAL))
    p.append(t("HomeSteady-TR-8821", CX + 64, y + 36, 16, DARK, "bold"))
    p.append(t("Serial HS-FAKE-001 · Firmware 1.0.0", CX + 64, y + 58, 12, GRAY))
    p.append(rect(CX1 - 190, y + 30, 166, 30, fill=GREEN_BG, stroke=GREEN, rx=15))
    p.append(t("✓  Online & Protected", CX1 - 107, y + 49, 13, GREEN, "bold", "middle"))
    y += h + 12
    # network card
    h = 110
    card(p, CX, y, CW, h)
    p.append(t("Uplink & VPN", CX + 24, y + 28, 15, DARK, "bold"))
    p.append(t("Wi-Fi", CX + 24, y + 56, 13, GRAY))
    p.append(t("HomeNet-5G", CX1 - 24, y + 56, 13, DARK, "bold", "end"))
    p.append(t("Router IP", CX + 24, y + 78, 13, GRAY))
    p.append(t("10.64.0.42", CX1 - 24, y + 78, 13, DARK, "bold", "end"))
    p.append(t("VPN", CX + 24, y + 100, 13, GRAY))
    p.append(t("Tailscale · exit node mullvad-us12 · Active", CX1 - 24, y + 100, 13, GREEN, "bold", "end"))
    y += h + 12
    y = sect(p, y, "Router controls")
    bw = (CW - 12) // 2
    y = btn(p, CX, y, bw, 50, "Change Wi-Fi", "primary")
    p.append(rect(CX + bw + 12, y - 50, bw, 50, fill=SLATE, stroke=SLATE, rx=25))
    p.append(ic_vpnlock(CX + bw + 12 + 30, y - 37))
    p.append(t("Stop VPN", CX + bw + 12 + 62, y - 19, 14, "#FFFFFF", "bold"))
    y += 10
    y = btn(p, CX, y, bw, 50, "↻  Reboot", "ghost")
    p.append(rect(CX + bw + 12, y - 50, bw, 50, fill="#FFFFFF", stroke=LINE, rx=25))
    p.append(t("Diagnostics", CX + bw + 12 + bw // 2, y - 19, 14, TEAL, "bold", "middle"))
    y += 10
    y = btn(p, CX, y, bw, 50, "Factory Reset", "danger-outline")
    p.append(rect(CX + bw + 12, y - 50, bw, 50, fill="#FFFFFF", stroke=LINE, rx=25))
    p.append(t("Disconnect", CX + bw + 12 + bw // 2, y - 19, 14, DARK, "bold", "middle"))
    y += 10
    y = annot(p, y, "Reboot and Factory Reset ask for confirmation first (O1). Diagnostics downloads a bundle.")
    return browser_close(p)

# ================= O1 — Confirm dialog (Factory Reset) =================
def frame_o1():
    p = frame_w5()
    svg = p
    inner = svg[:-len("</svg>")]
    inner += f'<rect x="0" y="76" width="1280" height="724" fill="#111827" opacity="0.45"/>'
    dx, dy, dw, dh = 430, 230, 420, 240
    inner += rect(dx, dy, dw, dh, fill="#FFFFFF", stroke=LINE, rx=16)
    inner += t("Factory Reset Travel Router?", dx + 24, dy + 36, 17, DARK, "bold")
    inner += t("This erases the Wi-Fi config and the", dx + 24, dy + 62, 13, GRAY)
    inner += t("VPN config. The router restarts.", dx + 24, dy + 82, 13, GRAY)
    inner += rect(dx + 24, dy + 150, 150, 46, fill="#FFFFFF", stroke=LINE, rx=23)
    inner += t("Cancel", dx + 99, dy + 178, 14, DARK, "bold", "middle")
    inner += rect(dx + 196, dy + 150, 200, 46, fill=RED, stroke=RED, rx=23)
    inner += t("Confirm Reset", dx + 296, dy + 178, 14, "#FFFFFF", "bold", "middle")
    inner += t("Reboot reuses this dialog: “Reboot Router?” / “Reboot Now”, not destructive.", dx + 24, dy + 222, 11, GRAY, "normal", "start", "italic")
    inner += "</svg>"
    return inner

# ================= O2 — Logs panel =================
def frame_o2():
    p = frame_w5()
    svg = p
    inner = svg[:-len("</svg>")]
    inner += f'<rect x="0" y="76" width="1280" height="724" fill="#111827" opacity="0.45"/>'
    dx, dy, dw, dh = 280, 130, 720, 480
    inner += rect(dx, dy, dw, dh, fill="#FFFFFF", stroke=LINE, rx=16)
    inner += t("Router logs", dx + 24, dy + 36, 17, DARK, "bold")
    inner += t("Live USB log — same events the router records.", dx + 24, dy + 58, 12, GRAY)
    inner += rect(dx + 24, dy + 72, dw - 48, 300, fill="#0F172A", stroke="#0F172A", rx=8)
    log_lines = [
        ("14:02:11.204", "usb", "device opened: HomeSteadyLink", "#7DD3FC"),
        ("14:02:14.802", "wifi", "scan: 3 networks", "#7DD3FC"),
        ("14:02:19.455", "wifi", "join HomeNet-5G: associated", "#7DD3FC"),
        ("14:02:21.090", "dhcp", "ip 10.64.0.42", "#7DD3FC"),
        ("14:02:24.518", "vpn", "tailscale up: BackendState=Running", "#7DD3FC"),
        ("14:02:26.003", "vpn", "exit node mullvad-us12: ping ok", "#7DD3FC"),
        ("14:02:26.104", "status", "online", "#4ADE80"),
    ]
    ly = dy + 96
    for ts, tag, msg, col in log_lines:
        inner += mono(dx + 40, ly, f"[{ts}] [{tag}] {msg}", 12, col)
        ly += 22
    inner += mono(dx + 40, ly + 8, "Empty state: “No log events yet.”", 12, GRAY, "start")
    inner += rect(dx + 24, dy + 396, 170, 40, fill="#FFFFFF", stroke=LINE, rx=20)
    inner += t("Copy logs", dx + 109, dy + 421, 13, DARK, "bold", "middle")
    inner += rect(dx + 206, dy + 396, 220, 40, fill=TEAL, stroke=TEAL, rx=20)
    inner += t("Download diagnostics", dx + 316, dy + 421, 13, "#FFFFFF", "bold", "middle")
    inner += rect(dx + dw - 124, dy + 396, 100, 40, fill="#FFFFFF", stroke=LINE, rx=20)
    inner += t("Close", dx + dw - 74, dy + 421, 13, DARK, "bold", "middle")
    inner += "</svg>"
    return inner

FRAMES = [
    ("flow-web", frame_flow),
    ("w1-connect", frame_w1),
    ("w1-unsupported", frame_w1_unsupported),
    ("w1-denied", frame_w1_denied),
    ("w2-wifi", frame_w2),
    ("w2-wifi-empty", frame_w2_empty),
    ("w3-vpn", frame_w3),
    ("w4-progress", frame_w4),
    ("w4-error", frame_w4_error),
    ("w5-device", frame_w5),
    ("o1-confirm", frame_o1),
    ("o2-logs", frame_o2),
]

if __name__ == "__main__":
    for name, fn in FRAMES:
        svg = fn()
        fpath = os.path.join(OUT, name + ".svg")
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(svg)
        print("wrote", fpath, len(svg), "bytes")
