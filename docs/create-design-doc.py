#!/usr/bin/env python3
"""Create the USB web-app design doc page under Home in Notion."""
import json
import subprocess

HOME_ID = "252ac25eb49f808e88a2d146612e3fda"

CONTENT = """# Design — USB web app (WebUSB)

Goal: a web page that controls the HomeSteadyLink router over USB, the same as the Android app. Status: design (Stage 2 of the USB pipeline). PRD: "PRD — Screens & Wireframes", section "Web app — USB control (WebUSB)". Nothing is implemented from this doc until the PRD is approved — Den ordered PRD → design → implement.

## Decisions

1. One daemon, two transports. `hsl-provisiond` gains a `--transport` flag (`ble`, `usb`, `both`; default `both`). The GATT handlers and the USB dispatcher call the same op functions, the same state files, the same Wi-Fi/VPN code. No duplicated logic, no second state machine.
2. FunctionFS vendor-specific interface on the existing gadget. No new gadget, no new VID/PID, no change to ACM/ECM/RNDIS behaviour.
3. The product string becomes `HomeSteadyLink` so the browser's device picker shows the router's name.
4. No encryption on the USB channel. Physical possession of the cable is the trust boundary; the 6-digit setup code is the authentication.
5. Pairing over USB uses an owner token. The web app generates a random 128-bit token, sends it with the setup code; the daemon stores it and requires it on every later command. Mirrors "first bonded peer is the only owner" without BLE.
6. The Tailscale auth key comes from the user. They generate it in the Tailscale admin console and paste it into the web app (W4). The firmware never bakes in a key.
7. Exit node is typed input in v1. The daemon verifies it with `tailscale ping` after `tailscale up`.
8. GitHub Pages is the host. Netlify is not used (token stale).

## USB interface

Current gadget (`firmware/systemd/setup-usb-gadget.sh`): configfs gadget `pi`, VID 0x1d6b, PID 0x0104, manufacturer `SteadyLink`, product `USB 10/100/1000 LAN`, serial `9810`, config `c.1` with `acm.usb0`, `ecm.usb0`, `rndis.usb0`. Microsoft OS descriptors on (`os_desc/use=1`, `MSFT100`, `b_vendor_code=0x01`). Brought up by `usb-gadget.service` (oneshot, `After=local-fs.target`, `Before=sysinit.target`).

Changes (Stage 3):

- Add `functions/ffs.usb0` to the same config `c.1`. FunctionFS, class 0xFF (vendor-specific), subclass 0x00, protocol 0x00. Two bulk endpoints: EP OUT (host → device) and EP IN (device → host), 512-byte max packet (USB 2.0 high-speed).
- Mount FunctionFS at `/dev/ffs-usb` (`modprobe usb_f_fs`, `mount -t functionfs usb /dev/ffs-usb`). Verify the module exists in the base image first — if `usb_f_fs` is absent from Armbian 25.5.1 (kernel 6.12.23), the build must add it before this works.
- Split the UDC bind out of `setup-usb-gadget.sh`. The script creates the gadget and links the functions but does NOT bind the UDC. `hsl-usbd` (part of `hsl-provisiond --transport usb`, started by a new `hsl-usbd.service` `After=usb-gadget.service`) writes the descriptors and strings to `/dev/ffs-usb/ep0`, then binds the UDC by writing its name into the gadget's `UDC` file. This is the standard FunctionFS order: descriptors must exist before the host enumerates the interface.
- Microsoft OS descriptors: extend the existing `os_desc` so Windows binds WinUSB to the vendor interface (compatible ID for `USB\\Class_FF&SubClass_00&Prot_00`). Linux and macOS need no driver — WebUSB claims the interface directly. Windows needs no manual driver install if the OS descriptor is right; if it is wrong, Windows shows the device with no driver and the page cannot claim it — this is a Stage 5 test item.
- Product string: `USB 10/100/1000 LAN` → `HomeSteadyLink`. Cosmetic for the Ethernet interfaces; it is what the browser picker shows.
- Interface number: the web app does NOT hardcode it. It reads the device configuration and claims the interface with class 0xFF. The firmware documents the expected number (3rd function in `c.1`, after ACM/ECM/RNDIS) for debugging only.

## Protocol

Framing: 4-byte big-endian length prefix + UTF-8 JSON payload. Max frame 64 KiB. The daemon reads exactly `length` bytes, parses the JSON, dispatches one op per frame, and replies with one frame. The web app sends one request at a time and waits for the reply (except status polling, which is one request per second during Progress).

Command set — same operations and JSON shapes as the GATT contract (`firmware/spec/gatt.md`, service 7f3a0000-1c2d-4e5f-8a9b-0c1d2e3f4a5b):

| USB op | GATT characteristic | Direction | Payload |
|---|---|---|---|
| `get_info` | DeviceInfo (read) | request/response | `{serial, firmware, model, state}` |
| `pair` | — (BLE uses Passkey Entry) | request/response | `{"code": "482913", "owner_token": "<128-bit hex>"}` |
| `scan_wifi` | WifiScan (read+notify) | request/response | list of `{ssid, bssid, rssi, band, security}` |
| `set_wifi` | WifiConfig (write) | request/response | `{ssid, psk, country, hidden, bssid?}` |
| `set_vpn` | VpnConfig (write) | request/response | exactly one of `{"type":"wireguard","conf":"..."}` or `{"type":"tailscale","authkey":"...","exit_node":"..."}` |
| `get_status` | Status (read+notify) | request/response, polled 1/s | `{state, error?, ssid?, ip?, vpn?}` |
| `control` | Control (write) | request/response | `{"cmd": "reboot" \| "factory_reset" \| "close_window" \| "vpn_stop" \| "vpn_start" \| "unbond" \| "portal_pass" \| "portal_recheck" \| "diagnostics"}` |

Notes:

- BLE uses notify for scan and status because BLE MTU is small. USB bulk has no such constraint: `scan_wifi` returns the whole list in one response (the web app waits up to 30 s); `get_status` is polled.
- Error replies are `{error: "<code>", detail: "<plain words>"}` using the same error codes as GATT: `auth_failed`, `timeout`, `bt_dead` (n/a on USB), `captive_portal`, `dhcp_failed`, `vpn_failed`, `vpn_not_full_tunnel`, `vpn_config_invalid`, `unsupported_eap`, `regdom_mismatch`, `authkey_expired`, `wifi_config_invalid`, `busy`, `internet_unreachable`, plus USB-only `not_owner` and `window_closed`.
- Status states are the same as GATT: `idle`, `scanning`, `wifi_joining`, `wifi_auth_failed`, `dhcp`, `internet_check`, `vpn_starting`, `online`, `online_no_vpn`, `vpn_failed`, `captive_portal`, `factory_reset`.
- The provisioning window (300 s after boot, permanently while no Wi-Fi is stored) is enforced in the daemon, not by the interface: after it closes, `get_info`/`get_status` still answer, but `pair`/`set_wifi`/`set_vpn` return `window_closed`. BLE stops advertising the service UUID; USB has no equivalent, so the daemon enforces it in software.
- `diagnostics` returns the same bundle as the BLE path (`/etc/homesteadlink/diag.tar.gz`).

## Pairing / auth

BLE pairing is Passkey Entry over the Bluetooth link. USB has no pairing, so the setup code is sent as a message:

1. The web app sends `{"op":"pair","code":"<6 digits>","owner_token":"<random 128-bit hex>"}`.
2. The daemon compares the code to `identity.json` (`/etc/homesteadlink/identity.json`, same file the BLE path uses). On match, it writes the owner token to `/etc/homesteadlink/owner.json` (0600, root only) and replies `{"paired": true}`. On mismatch it counts the failure — same lockout as BLE: 5 failures → 15-minute lockout, then 30, then 60, powered-on time only — and replies `auth_failed` with the attempts left.
3. Every later command includes the owner token. The daemon rejects a missing or wrong token with `not_owner`. `control unbond` clears `owner.json` (same as the BLE unbond).
4. Only the first paired browser owns the router. A second browser that pairs with the right code replaces the owner — same as BLE re-bonding after unbond. The setup code is the only credential; anyone with the code and the cable owns the device.

## Tailscale

- The firmware enables `tailscaled` but bakes in NO auth key (verified: no auth key, `tailscale up`, or `TS_AUTHKEY` anywhere in the build). The auth key comes from the user: they generate it in the Tailscale admin console (Settings → Keys) and paste it into the web app (W4, field `Auth key (tskey-auth-…)`).
- The web app sends it as `VpnConfig {"type":"tailscale","authkey":"tskey-auth-…","exit_node":"<optional>"}`. The daemon stores it at `/etc/homesteadlink/.ts-authkey` (0600, root only) and runs `tailscale up --authkey file:/etc/homesteadlink/.ts-authkey --accept-dns=false` (existing `vpn.go` code, unchanged).
- The key is consumed once. After that the board's Tailscale state lives in `/var/lib/tailscale` and survives reboots with no new key. A factory reset wipes it — a new key is needed.
- Exit node: typed input in v1 (the board cannot list the tailnet's exit nodes before it joins). The daemon verifies the choice with `tailscale ping <exit_node>` after `tailscale up` (existing `vpn.go` code). A bad node → `vpn_failed`; an expired key → `authkey_expired`.
- Online means: `tailscaled` BackendState=Running, `tailscale netcheck` UDP OK, and a successful `tailscale ping` to the exit node when one is set. `tailscale-wait-online.service` (`tailscale wait`) gates on BackendState=Running.
- Out of scope for v1: listing the tailnet's exit nodes in the web app (needs the board online first; the Device screen can offer it later from `tailscale status --json`).

## Web app

- One `index.html` in `HomesteadLink/web-app`, plain JS + WebUSB, no build step, no dependencies. Same file layout as the PRD: Connect → Pair → Wi-Fi → VPN → Progress → Device.
- Flow: `navigator.usb.requestDevice({filters: [{vendorId: 0x1d6b, productId: 0x0104}]})` → `open()` → `selectConfiguration(1)` → find the interface with class 0xFF → `claimInterface(n)` → bulk OUT/IN endpoints. Send one framed JSON request, read one framed response. Poll `get_status` once per second during Progress.
- HTTPS required: WebUSB needs a secure context. GitHub Pages serves HTTPS. `http://localhost` also counts as a secure context for local dev.
- Browser support: Chrome and Edge on macOS, Windows, Linux (full WebUSB); Android Chrome with a USB cable; Safari and Firefox have no WebUSB — fallback is the router's Wi-Fi setup page (http://192.168.65.1:8080).
- The device picker is the browser's own dialog — the page cannot draw, style, or log it. Closing the tab disconnects USB; the page keeps the paired device for the browser session only. The setup code, Wi-Fi password, and auth key live in page memory only and are never stored in the browser.
- The web app never stores secrets in `localStorage` or cookies. The owner token lives in page memory for the session.

## Hosting

GitHub Pages, primary: https://homesteadlink.github.io/web-app/ (repo `HomesteadLink/web-app`, Pages source `main`, root). No build step — the page is served as-is. Netlify is NOT used: its token is stale and its deploy is blocked; do not block on it.

## Security

- Trust boundary: physical possession of the USB cable. The channel is not encrypted; anyone with the cable and the setup code owns the device. This matches the threat model of typing the code into the browser on the user's own computer.
- Secrets on the board are 0600 root-only: `/etc/homesteadlink/.ts-authkey`, `/etc/homesteadlink/owner.json`, `/etc/homesteadlink/device-secret`, Wi-Fi PSK in `/etc/homesteadlink/wifi.conf`.
- Secrets are never logged. The daemon logs only fingerprints (length + first 4 bytes of SHA-256), the existing `fingerprint()` rule in `hsl-provisiond`.
- The setup code is never stored in the browser; the Wi-Fi password and auth key are not either.
- Lockout: 5 wrong codes → 15 min, then 30, cap 60, powered-on time only — same as BLE.
- Provisioning window enforced in the daemon (see Protocol).
- The kill switch is unchanged: a bad VPN config fails closed (no internet without VPN). `set_vpn` is validated before applying.

## Test plan

Stage 3 (firmware, this VM + rebuild pipeline):

- The image rebuilds; size + sha256 recomputed; Stage 6-style checks pass.
- `usb_f_fs` is present in the image (module under `/lib/modules/*/kernel/drivers/usb/gadget/` or built-in). If absent, the build adds it.
- The gadget enumerates with 4 functions in config `c.1` (ACM, ECM, RNDIS, FFS) — verified by `lsusb -v` on the MacBook after flashing.
- `hsl-usbd` writes descriptors and binds the UDC; `/dev/ffs-usb/ep0` exists after boot.

Stage 5 (flash + end-to-end, needs Den's hands for the SD swap):

- Flash the new image via the MacBook (Den powers off the board, takes the SD out, puts it in the MacBook's reader, puts it back).
- Open https://homesteadlink.github.io/web-app/ in desktop Chrome, connect over USB, pair with the setup code (needs HSL-IDENTITY from Den), scan and discover Wi-Fi networks, connect to one, show the board online.
- Windows: the vendor interface binds WinUSB via the OS descriptor with no manual driver install.
- Tailscale: Den generates an auth key in the Tailscale admin console (a credential only he can supply); the board joins the tailnet and the exit node pings OK.
- Negative cases: wrong setup code (lockout counts), no networks found, Wi-Fi auth failed, expired auth key.
- Emulator cannot test this (no USB passthrough, no BLE radio). The real board is the only test.

## Open items / risks

1. `usb_f_fs` may be absent from the Armbian base image — Stage 3 must check and add it if needed.
2. Windows WinUSB binding depends on the OS descriptor being exactly right; if it is wrong, Windows shows the device with no driver and the page cannot claim it. Stage 5 tests this on a Windows machine if one is available; otherwise it is documented as untested on Windows.
3. The PRD has no frame for Tailscale auth-key expiry or for the captive-portal pass flow on the web app — both are named states on W5-error, but the frames do not exist yet. Add them to the PRD before build if they need drawing.
4. The exit-node picker is free text in v1 (PRD audit flag #4) — decided here as typed input, verified by `tailscale ping`.
5. HSL-IDENTITY (setup code + console password) is still pending from Den — it blocks the Stage 5 pairing test.

## Sources

- PRD: "PRD — Screens & Wireframes", section "Web app — USB control (WebUSB)" (14 frames).
- GATT contract: `HomesteadLink/firmware` `spec/gatt.md` (service 7f3a0000-1c2d-4e5f-8a9b-0c1d2e3f4a5b, 6 characteristics).
- Daemon: `HomesteadLink/firmware` `hsl-provisiond/` (`main.go`, `vpn.go`, `gatt.go` — state files under `/etc/homesteadlink/`, fingerprint logging rule).
- Gadget: `HomesteadLink/firmware` `systemd/setup-usb-gadget.sh` + `usb-gadget.service` (configfs gadget `pi`, VID 0x1d6b PID 0x0104, ACM+ECM+RNDIS, MS OS descriptors).
- Tailscale online gate: `tailscale-wait-online.service` (`tailscale wait`).
- Web app repo: `HomesteadLink/web-app` (commit 193d361, PRD wireframes).
- Hosted at: https://homesteadlink.github.io/web-app/ (GitHub Pages, Stage 4).
"""

args = {
    "allow_async": False,
    "parent": {"type": "page_id", "page_id": HOME_ID},
    "pages": [{
        "properties": {"title": "Design — USB web app (WebUSB)"},
        "content": CONTENT,
    }],
}
cmd = ["/opt/hatch/bin/notion-cli", "call-tool", "--name", "notion-create-pages",
       "--arguments-json", json.dumps(args)]
r = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
print("rc:", r.returncode)
print(r.stdout[:3000])
print(r.stderr[:1000])
