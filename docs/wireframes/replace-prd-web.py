#!/usr/bin/env python3
"""Replace the web-app section of the Notion PRD page (no-setup-code version).
Fetches the page, keeps everything before '## Web app — USB control (WebUSB)',
appends the new section, and replace_content's the whole block.
Reads web-wireframe-uploads.json for the image URLs.
"""
import json
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
PRD_URL = "https://app.notion.com/p/418ac25eb49f812eb47be127c5a96458"
MARKER = "## Web app — USB control (WebUSB)"

with open(os.path.join(HERE, "web-wireframe-uploads.json")) as f:
    up = json.load(f)

def img(name):
    return f'<image source="{up[name]}" />'

def call(tool, args):
    cmd = ["/opt/hatch/bin/notion-cli", "call-tool", "--name", tool,
           "--arguments-json", json.dumps(args)]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    if r.returncode != 0:
        raise RuntimeError(f"{tool} failed: {r.stdout} {r.stderr}")
    return json.loads(r.stdout)

NEW_SECTION = f"""## Web app — USB control (WebUSB)

A web page that controls the router over USB, the same as the Android app. Desktop Chrome and Edge on macOS, Windows, and Linux. Safari can't use USB — its fallback is the router's Wi-Fi setup page (http://192.168.65.1:8080). No setup code anywhere in this flow: the USB cable is the trust — anyone holding the board and a cable can control it. That is the point, and it matches how USB hardware works. The setup code stays for BLE only, because BLE is wireless. Nothing is implemented from this section until Den approves.

## Web product

The web app is the same product as the Android app on a second control path: instead of Bluetooth, the page talks to the router over a USB cable (WebUSB). The router exposes a vendor-specific USB interface (FunctionFS); the page sends the same operations the Android app sends over GATT — Wi-Fi scan and config, VPN config, status, control. One wizard, one decision per step, same as the Android flow, minus Pair: there is no pairing step, because there is no code to enter. Plug the cable in and the page works.

## Web browser support

- Chrome and Edge on macOS, Windows, Linux: full WebUSB.
- Android Chrome: works with a USB cable (USB-OTG).
- Safari (macOS, iOS) and Firefox: no WebUSB. Fallback: join the "HomeSteady-…" Wi-Fi network, open http://192.168.65.1:8080.
- The page is served over HTTPS (WebUSB needs a secure context). Hosted at https://homesteadlink.github.io/web-app/.

## Web flow

{img("flow-web")}

Connect (pick the router in the browser's device picker) → Wi-Fi (networks near the router) → VPN (WireGuard / Tailscale / Skip) → Progress (live status) → Device (steady-state control). The device picker is the browser's own dialog — the page cannot draw it. Closing the tab disconnects; unplugging the cable disconnects too. Plug it back in and the page works again — no code, no re-pairing.

## W1 — Connect

Why: let the user pick the router over USB.

{img("w1-connect")}

The page shows the cable state and opens the browser's device picker. Picking "HomeSteadyLink" goes to Wi-Fi. Cancelling the picker returns here.

## W1 — Browser not supported (error state)

Why: Safari and Firefox have no WebUSB — the user must know why the page can't work, and what to do instead.

{img("w1-unsupported")}

Full error behind "Copy error details": the browser name and version, the missing API (navigator.usb), and the fallback link. Next action: open the page in Chrome or Edge, or use the Wi-Fi setup page.

## W1 — No router found (error state)

Why: the cable, the picker, or the browser's USB permission can each fail — the user needs the checklist, not a blank page.

{img("w1-denied")}

Full error behind "Copy error details": the USB error name and the browser's reason, copied as one block for a bug report. Next action: check the cable, pick the device again.

## W2 — Wi-Fi

Why: pick a network the router can see, and give its password.

{img("w2-wifi")}

The list comes from the router's scan (tap a row to fill the SSID). Password is masked with an eye toggle. Hidden SSID and country live under Advanced (country prefilled from the computer's locale). Nothing is written to the router yet — Connect sends Wi-Fi + VPN together on the next step.

## W2 — No networks found (empty state)

Why: an empty scan is a state of its own — the user needs a next step, not an empty list.

{img("w2-wifi-empty")}

Full error behind "Copy error details": the scan result (0 networks) and the router state. Next action: move the router closer to a Wi-Fi network and scan again, or type a network name instead (works for hidden networks too).

## W3 — VPN

Why: take a WireGuard .conf or a Tailscale auth key + exit node — or skip VPN.

{img("w3-vpn")}

Two stacked cards, not tabs: WireGuard first (paste or upload the .conf, masked with an eye toggle), Tailscale second (auth key field, exit node field, optional). Pick one; the other stays empty. Save sends Wi-Fi + VPN together → Progress. Skip sends Wi-Fi only.

## W4 — Progress

Why: show live provisioning status while the router joins Wi-Fi and starts the VPN.

{img("w4-progress")}

The page polls the router over USB — every step updates live, no refresh. Steps: USB link, Joining Wi-Fi, Internet check, Starting VPN. "Back to Wi-Fi setup" is replaced by "Open device dashboard" once the router is online.

## W4 — Wi-Fi failed (error state)

Why: the most common failure must say what happened in plain words first, with the full detail behind a copy button.

{img("w4-error")}

Full error behind "Copy error details": error code, state, SSID, BSSID, signal, device serial and firmware. Next action: re-enter the Wi-Fi password. The old config still works if one was saved. Other errors use this same card: captive portal, VPN failed, no internet.

## W5 — Device dashboard

Why: steady-state control of a provisioned router.

{img("w5-device")}

Status card (serial, firmware, Online & Protected), uplink & VPN card (Wi-Fi, router IP, VPN type + exit node), controls in two columns: Change Wi-Fi, Stop/Start VPN, Reboot, Diagnostics, Factory Reset, Disconnect. Reboot and Factory Reset ask for confirmation first (O1). Stop VPN shows the VpnLock icon when VPN is active.

## O-W1 — Confirm dialog (Factory Reset)

Why: destructive actions need an explicit confirm before the router wipes itself.

{img("o1-confirm")}

Centered dialog over a dimmed page. Reboot reuses this dialog: "Reboot Router?" / "Reboot Now", non-destructive. Disconnect shows no dialog.

## O-W2 — Logs panel

Why: live USB telemetry for debugging provisioning; opened from Diagnostics.

{img("o2-logs")}

The panel slides over the dimmed page. Log lines are monospace; the online line renders green, errors red. Empty state: "No log events yet." Copy logs and Download diagnostics buttons at the bottom.

## Web Safari divergence

- Safari (macOS, iOS) has no WebUSB and no WebSerial — the web app cannot control the router from Safari at all. The fallback is the router's Wi-Fi setup page (http://192.168.65.1:8080), which works in any browser.
- Firefox has no WebUSB either — same fallback.
- The browser's device picker is native browser chrome on every platform — the page cannot style it, log it, or draw it.
- Closing the tab or unplugging the cable disconnects USB. The Android app keeps the BLE bond across launches; the web app trusts the cable instead — plug it back in and it works again, no code, no re-pairing.

## Web audit flags

1. The design doc's pairing/auth section was rewritten for the redirect (Den, 2026-11-15): no setup code, no owner token — USB presence is the trust root. The design doc (Stage 2) carries the full mechanism.
2. No screen for the Tailscale auth-key expiry (error=authkey_expired) — needs a frame or a named state on W4-error before build.
3. No screen for the captive-portal pass flow on the web app (Android has it on Progress) — needs a frame before build.
4. The exit-node picker is a free-text field in W3 — the design must say whether the page lists the tailnet's exit nodes or takes typed input.
5. The logs panel shows router-side events; the page's own USB errors (disconnect mid-flow) have no drawn state yet.

## Web sources

- Repo: HomesteadLink/web-app, docs/wireframes/ (SVGs are the source; PNGs are never committed). 12 frames: flow + W1–W5 + error/empty states + 2 overlays.
- GATT contract: HomesteadLink/firmware spec/gatt.md (service 7f3a0000-1c2d-4e5f-8a9b-0c1d2e3f4a5b, 6 characteristics).
- Android screens this mirrors: S1, S3–S6, O1–O2 on this page (no Pair — the web app has no setup code).
- Hosted at: https://homesteadlink.github.io/web-app/ (GitHub Pages, Stage 4).
"""

# Fetch current page content — the fetch result wraps the page Markdown in
# <page>...<content>...</content></page>; replace_content takes only the
# inner <content> Markdown.
res = call("notion-fetch", {"id": "418ac25e-b49f-812e-b47b-e127c5a96458"})
report = json.loads(res["content"][0]["text"])["text"]
start = report.index("<content>") + len("<content>")
end = report.rindex("</content>")
inner = report[start:end]
if MARKER not in inner:
    raise RuntimeError("web section marker not found in PRD")
head = inner[:inner.index(MARKER)]
new_content = head.rstrip() + "\n\n" + NEW_SECTION

res2 = call("notion-update-page", {
    "allow_async": False,
    "page_id": PRD_URL,
    "command": "replace_content",
    "new_str": new_content,
})
print("replace rc:", res2.get("ok"), json.dumps(res2)[:500])
print("new content chars:", len(new_content))
print("old web images removed; new images:", new_content.count("<image"))
