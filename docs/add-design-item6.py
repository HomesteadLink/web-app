#!/usr/bin/env python3
"""Add design-doc open item 6: Diagnostics download is trigger-only in v1."""
import json, subprocess

DESIGN_URL = "https://app.notion.com/p/419ac25eb49f81b4b4cbd65a56b618cc"

OLD = "5. HSL-IDENTITY is no longer needed for the webapp (Den does not know it; do not ask again). It is still the BLE credential. Recovery path: a fresh firmware image regenerates the identity at first boot — capture the new line live on the serial console during that boot. The BLE P1–P16 test still lists the identity as needed; treat it as unavailable until that capture happens."
NEW = OLD + "\n6. Diagnostics download is trigger-only in v1 (Stage 4). The web app's Diagnostics button runs the <code>diagnostics</code> control op, which builds the bundle on the board at <code>/etc/homesteadlink/diag.tar.gz</code>, but there is no <code>get_diagnostics</code> op to download it over USB, so the page says so and points at the Wi-Fi setup page / serial console. A chunked download op (base64 chunks under the 64 KiB frame cap) is a v1.1 addition — it needs a daemon op, a design-protocol row, and a web-app change."

args = {"allow_async": False, "page_id": DESIGN_URL, "command": "update_content",
        "content_updates": [{"old_str": OLD, "new_str": NEW}]}
cmd = ["/opt/hatch/bin/notion-cli", "call-tool", "--name", "notion-update-page",
       "--arguments-json", json.dumps(args)]
r = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
print("rc:", r.returncode)
print(r.stdout[:1200])
print(r.stderr[:500])
