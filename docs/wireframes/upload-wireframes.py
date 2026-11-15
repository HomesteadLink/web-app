#!/usr/bin/env python3
"""Upload web wireframe SVGs to Notion and record their file-upload URLs.
Usage: python3 upload-wireframes.py  (writes web-wireframe-uploads.json)
Uploads expire in ~1h if unattached — place them on the PRD right after.
"""
import json
import subprocess
import sys
import os

WIRE = os.path.dirname(os.path.abspath(__file__))
NAMES = ["flow-web", "w1-connect", "w1-unsupported", "w1-denied", "w2-wifi",
         "w2-wifi-empty", "w3-vpn", "w4-progress", "w4-error", "w5-device",
         "o1-confirm", "o2-logs"]

def call(tool, args):
    cmd = ["/opt/hatch/bin/notion-cli", "call-tool", "--name", tool,
           "--arguments-json", json.dumps(args)]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if r.returncode != 0:
        raise RuntimeError(f"{tool} failed: {r.stdout} {r.stderr}")
    return json.loads(r.stdout)

out = {}
for name in NAMES:
    path = os.path.join(WIRE, name + ".svg")
    with open(path, encoding="utf-8") as f:
        svg = f.read()
    print(f"uploading {name}.svg ({len(svg)} bytes)...", flush=True)
    res = call("notion-create-attachment", {"content": svg, "filename": name + ".svg"})
    # find markdown_source in the result (it is nested inside a
    # JSON-encoded string in the text field, so match the URL directly)
    import re
    m = re.search(r'file-upload://[0-9a-f-]{36}', json.dumps(res))
    if not m:
        print("RESULT:", json.dumps(res)[:2000])
        raise RuntimeError(f"no markdown_source for {name}")
    src = m.group(0)
    if not src:
        print("RESULT:", json.dumps(res)[:2000])
        raise RuntimeError(f"no markdown_source for {name}")
    out[name] = src
    print(f"  -> {src}", flush=True)

with open(os.path.join(WIRE, "web-wireframe-uploads.json"), "w") as f:
    json.dump(out, f, indent=2)
print("wrote web-wireframe-uploads.json")
