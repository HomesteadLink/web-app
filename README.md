# HomeSteadyLink web app

Control the HomeSteadyLink travel router over USB (WebUSB) — the same
product as the Android app, on a second control path.

- **What it does:** connect to the router over a USB cable, pair with the
  6-digit setup code, list Wi-Fi networks and connect, set up the VPN
  (WireGuard or Tailscale with an exit node), and control the device.
- **Browsers:** Chrome and Edge on macOS, Windows, Linux; Android Chrome
  with a USB cable. Safari and Firefox have no WebUSB — the fallback is
  the router's Wi-Fi setup page (http://192.168.65.1:8080).
- **Hosting:** GitHub Pages — https://homesteadlink.github.io/web-app/
- **PRD:** Notion, "PRD — Screens & Wireframes", section
  "Web app — USB control (WebUSB)". Wireframe SVGs are the source and
  live in `docs/wireframes/` (PNG renders are never committed).
- **Design doc:** Notion (Stage 2 of the USB pipeline).
- **Status:** PRD done (Stage 1). Implementation follows the design doc.

## Layout (Stage 4)

- `index.html` — the app (single file, plain JS + WebUSB, no build step).
- `docs/wireframes/` — PRD wireframes (SVG source).
