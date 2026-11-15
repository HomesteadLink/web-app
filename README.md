# HomeSteadyLink web app

Control the HomeSteadyLink travel router over USB (WebUSB) — the same
product as the Android app, on a second control path.

- **What it does:** connect to the router over a USB cable, list Wi-Fi
  networks and connect, set up the VPN (WireGuard or Tailscale with an
  exit node), and control the device. No setup code anywhere in this
  flow — physical USB presence is the trust root (Den, 2026-11-15);
  the setup code stays for BLE only.
- **Browsers:** Chrome and Edge on macOS, Windows, Linux; Android Chrome
  with a USB cable. Safari and Firefox have no WebUSB — the fallback is
  the router's Wi-Fi setup page (http://192.168.65.1:8080).
- **Hosting:** GitHub Pages — https://homesteadlink.github.io/web-app/
- **PRD:** Notion, "PRD — Screens & Wireframes", section
  "Web app — USB control (WebUSB)". Wireframe SVGs are the source and
  live in `docs/wireframes/` (PNG renders are never committed).
- **Design doc:** Notion (Stage 2 of the USB pipeline).
- **Status:** Live (Stage 4, 2026-11-15). `index.html` at
  https://homesteadlink.github.io/web-app/ — verified HTTP 200, served
  bytes identical to the repo file. All 6 screens verified by
  headless-Chrome screenshots (0 console errors). Firmware v1.4.0
  (FunctionFS USB daemon) building; flash + end-to-end test is Stage 5.

## Layout (Stage 4)

- `index.html` — the app (single file, plain JS + WebUSB, no build step).
- `docs/wireframes/` — PRD wireframes (SVG source).
