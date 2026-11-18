# Play screenshot cards — HomeSteadyLink (1080×1920)

Branded store cards for the Google Play listing, built 2026-11-18
(Den's order: "best App Store Optimization marketing/card", not just
screenshots). One benefit headline per card, brand navy #0A0B3B +
cyan #00E5FF, style Bold, tagline "Your home network, anywhere you go".

**v2 (2026-11-18, regenerated after Den: "design sucks")** — rebuilt with
the ParthJadhav `app-store-screenshots` editor (vendored skill), style
**Midnight Glow Pro, cyan-beam adaptation**: near-black navy void,
cyan spotlight from above, Inter Tight 600 headlines with a white→grey
gradient and one cyan-lit word per card, mono eyebrow labels
(`01 / SCAN` …), real device bezel with shadow + glow. Editor project:
`~/workspace/homesteadylink/card-editor/` (`app-store-screenshots.json`
deck, `clean-wireframes.py`, `render-wireframes.cjs`, `export-deck.cjs`).
Headline scale 1.0; device-bottom captions shifted +50 px so 2-line
headlines clear the phone bezel.

| # | File | Headline | Screen |
|---|------|----------|--------|
| 1 | 01-scan-home-network.png | Home network, anywhere you go | Scan — REAL v3 emulator capture (real flavor) |
| 2 | 02-vpn-kill-switch.png | Kill switch on. Nothing leaks. | VPN — WireGuard/Tailscale, masked config |
| 3 | 03-device-control.png | Router control, from anywhere. | Device — status, VPN toggle, controls |
| 4 | 04-wifi-pick-network.png | Join any Wi-Fi in seconds. | Wi-Fi — pick network, enter password |
| 5 | 05-pair-one-code.png | One code pairs your router. | Pair — 6-digit setup code |

Order follows the app-store-optimization skill: slot 1 primary value,
slot 2 core differentiator (VPN + kill switch), slot 3 next strongest
feature (device control), slots 4–5 supporting setup steps. File
number = Play slot number — upload in filename order. Every caption
is benefit-oriented, 2–5 words. Card 1's headline is the brand
tagline trimmed to 5 words ("Your" dropped); the verbatim 6-word
tagline stays on the feature graphic and in the listing copy.

## Source (provenance — read before replacing)

Card 1 is a **real capture**: the v3 real-flavor emulator run
(`~/workspace/homesteadylink/emu-v3/shot-real-scan.png`, 1080×2400),
showing the shipped Scan screen with the "Scan again" button and the
"Don't have a board? Let's order one" link (PR #78). Cards 2–5 use the
**approved wireframe** from `HomesteadLink/mobile-app` `docs/wireframes/`
(PR #67, redrawn post-simplicity), cleaned for public use — the raw
wireframes carry a "FAKE DEVICE MODE" banner, a service UUID, a BLE MAC
and drafting notes, which were stripped (v2 cleaning script:
`~/workspace/homesteadylink/card-editor/clean-wireframes.py`; v1:
`~/workspace/homesteadylink/aso-cards/build/clean-svgs.py`). The s3
helper line "Using your phone's Wi-Fi network …" is genuine UI copy and
was kept. No clean live capture exists yet for VPN/Device/Wi-Fi/Pair
(the board test hasn't happened; the PR #40 emulator shots carry the
FAKE DEVICE banner and must never be used publicly). When clean live
captures exist, swap them in and update this file.

## Critic verdicts (growth-design, 2026-11-18, v2)

All 5 cards: **PASS** — Check 1 KPI (each shows the value that makes
a user install; card 1 carries the biggest promise; slot 2 is the core
differentiator per the app-store-optimization skill), Check 2 product
(every element verified against the shipped app/listing copy; no
feature shown that doesn't exist; no verified-pairing claim), Check 3
brand (same two colors, same tagline, Bold, same wordmark as the
feature graphic v3 and the landing). Headlines checked by reading the
renders at full size and at 220 px (thumbnail test: style, app purpose
and benefit all read at 220 px). Quality-bar §10 checks pass: no
clipped text, no headline collision with the phone bezel (fixed by
headline scale 1.0 + caption shift on device-bottom slides), no empty
band >22%, no fake claims.

v1 verdicts (same date, earlier run): also 5× PASS, same checks; v1 was
replaced on design grounds (flat navy, no bezel, no designed
background), not on a critic FAIL. Slot order unchanged from v1
(slot 1 primary value, slot 2 core differentiator, slot 3 next
strongest feature; all captions benefit-oriented, 2–5 words).
Card 1's headline is the tagline trimmed to 5 words ("Your" dropped);
the verbatim 6-word tagline stays on the feature graphic and in the
listing copy.

## Build

v2: ParthJadhav `app-store-screenshots` editor, scaffolded at
`~/workspace/homesteadylink/card-editor/` (Next.js, `npm install`,
`npm run build`, `npm run start -p 3000`, headless export via
Playwright `export-deck.cjs` → `~/workspace/homesteadylink/card-export/`).
Style implemented in the scaffolded copy only (never in the vendored
skill): `midnight-glow-cyan` theme, Inter Tight 600 + Geist Mono
fonts, gradient headline with `*word*` lit-word parsing in
`slide-canvas.tsx`. v1: HTML composition rendered with headless
Chromium 157 via CDP (`~/workspace/homesteadylink/aso-cards/build/`).
Final PNGs also at `~/workspace/homesteadylink/aso-cards/`.
