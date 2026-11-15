# docs/wireframes — web app wireframes

Hand-built SVG wireframes for the HomeSteadyLink web app (USB / WebUSB),
matching the Notion PRD section "Web app — USB control (WebUSB)".

- **SVGs are the source.** Hand-built, text-diffable, committed here.
  Regenerate: `python3 build-web-wireframes.py`.
- **PNGs are renders only.** Rendered for Notion and visual review via
  `node cdp-shot.js file://$PWD/<name>.svg $PWD/<name>.png 1280 800`
  (needs the headless-Chrome CDP instance on port 9222). PNGs are NEVER
  committed.
- Frames: flow-web, w1-connect, w1-unsupported, w1-denied, w2-pair,
  w2-pair-error, w3-wifi, w3-wifi-empty, w4-vpn, w5-progress, w5-error,
  w6-device, o1-confirm, o2-logs (14 frames, desktop browser 1280x800).
