# Play screenshot cards — HomeSteadyLink (1080×1920)

Branded store cards for the Google Play listing, built 2026-11-18
(Den's order: "best App Store Optimization marketing/card", not just
screenshots). One benefit headline per card, brand navy #0A0B3B +
cyan #00E5FF, style Bold, tagline "Your home network, anywhere you go".

| # | File | Headline | Screen |
|---|------|----------|--------|
| 1 | 01-scan-home-network.png | Home network, anywhere you go | Scan — finds the router, Connect |
| 2 | 02-vpn-kill-switch.png | Kill switch on. Nothing leaks. | VPN — WireGuard/Tailscale, masked config |
| 3 | 03-device-control.png | Control your router from anywhere | Device — status, VPN toggle, controls |
| 4 | 04-wifi-pick-network.png | Join any Wi-Fi in seconds | Wi-Fi — pick network, enter password |
| 5 | 05-pair-one-code.png | One code pairs your router | Pair — 6-digit setup code |

Order follows the app-store-optimization skill: slot 1 primary value,
slot 2 core differentiator (VPN + kill switch), slot 3 next strongest
feature (device control), slots 4–5 supporting setup steps. File
number = Play slot number — upload in filename order. Every caption
is benefit-oriented, 2–5 words. Card 1's headline is the brand
tagline trimmed to 5 words ("Your" dropped); the verbatim 6-word
tagline stays on the feature graphic and in the listing copy.

## Source (provenance — read before replacing)

The phone UI on each card is the **approved wireframe** from
`HomesteadLink/mobile-app` `docs/wireframes/` (PR #67, redrawn
post-simplicity), cleaned for public use — the raw wireframes carry a
"FAKE DEVICE MODE" banner and drafting notes, which were stripped
(see the cleaning script in `~/workspace/homesteadylink/aso-cards/build/clean-svgs.py`).
Fidelity fixes vs. the shipped app, verified against the code:
Pair subtitle shows just the BLE address (PairScreen.kt:99); Device
serial is the app fallback HS-DEMO-001; VPN config shows the masked
display the app shows by default. Card 1 also carries the real v3
order link ("Don't have a board? Let's order one", PR #78).

These are **cards built from the approved design, not live
screenshots** — no clean live capture exists yet (the board test
hasn't happened; the PR #40 emulator shots carry the FAKE DEVICE
banner and must never be used publicly). When the v3 emulator
evidence is clean, swap these for live captures and update this file.

## Critic verdicts (growth-design, 2026-11-18)

All 5 cards: **PASS** — Check 1 KPI (each shows the value that makes
a user install; card 1 carries the biggest promise), Check 2 product
(every element verified against the shipped app/listing copy; no
feature shown that doesn't exist; no verified-pairing claim), Check 3
brand (same two colors, same tagline, Bold, same wordmark as the
feature graphic v3 and the landing). Headlines checked by reading the
renders at full size and at 300 px (Play search size).

Re-ordered 2026-11-18 per the app-store-optimization skill (slot 1
primary value, slot 2 core differentiator, slot 3 next strongest
feature; all captions benefit-oriented, 2–5 words). First-fold
preview (slots 1–3 side by side at 300 px) verified: three distinct
benefits, captions readable, no onboarding/splash screen in the
first 3. Card 1's headline is the tagline trimmed to 5 words; the
verbatim 6-word tagline stays on the feature graphic and in the
listing copy.

## Build

Cards are composed as HTML (1080×1920) and rendered with headless
Chromium 157 via CDP. Sources: `~/workspace/homesteadylink/aso-cards/build/`
(clean-svgs.py, make-cards.py, cdp-card-shots.js, run.sh). Final PNGs
also at `~/workspace/homesteadylink/aso-cards/`.
