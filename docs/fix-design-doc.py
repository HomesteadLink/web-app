#!/usr/bin/env python3
"""Fix the design doc: single daemon (no hsl-usbd.service), usb_f_fs
verified present, web-app commit ref. Uses update_content with the exact
stored text (Notion stores backticks as <code> tags)."""
import json
import subprocess

DESIGN_URL = "https://app.notion.com/p/419ac25eb49f81b4b4cbd65a56b618cc"

UPDATES = [
    {
        "old_str": "Split the UDC bind out of <code>setup-usb-gadget.sh</code>. The script creates the gadget and links the functions but does NOT bind the UDC. <code>hsl-usbd</code> (part of <code>hsl-provisiond --transport usb</code>, started by a new <code>hsl-usbd.service</code> <code>After=usb-gadget.service</code>) writes the descriptors and strings to <code>/dev/ffs-usb/ep0</code>, then binds the UDC by writing its name into the gadget's <code>UDC</code> file. This is the standard FunctionFS order: descriptors must exist before the host enumerates the interface.",
        "new_str": "Split the UDC bind out of <code>setup-usb-gadget.sh</code>. The script creates the gadget and links the functions but does NOT bind the UDC. <code>hsl-provisiond</code> itself (USB transport, one daemon, two transports — no second service) writes the descriptors and strings to <code>/dev/ffs-usb/ep0</code>, then binds the UDC by writing its name into the gadget's <code>UDC</code> file. <code>hsl-provisiond.service</code> is ordered <code>After=usb-gadget.service</code> so the gadget exists first; the daemon waits for <code>/dev/ffs-usb/ep0</code> to appear. This is the standard FunctionFS order: descriptors must exist before the host enumerates the interface. If the daemon restarts, the gadget is already bound, so the descriptor write is skipped and the endpoints are opened directly.",
    },
    {
        "old_str": "Mount FunctionFS at <code>/dev/ffs-usb</code> (<code>modprobe usb_f_fs</code>, <code>mount -t functionfs usb /dev/ffs-usb</code>). Verify the module exists in the base image first — if <code>usb_f_fs</code> is absent from Armbian 25.5.1 (kernel 6.12.23), the build must add it before this works.",
        "new_str": "Mount FunctionFS at <code>/dev/ffs-usb</code> (<code>modprobe usb_f_fs</code>, <code>mount -t functionfs usb /dev/ffs-usb</code> — done by <code>setup-usb-gadget.sh</code>). Verified (Stage 3): <code>usb_f_fs.ko</code> is present in the base image (<code>/lib/modules/6.12.23-current-sunxi64/kernel/drivers/usb/gadget/function/usb_f_fs.ko</code>; <code>CONFIG_USB_FUNCTIONFS=m</code>, <code>CONFIG_CONFIGFS_FS=y</code>) — no kernel change needed.",
    },
    {
        "old_str": "1. <code>usb_f_fs</code> may be absent from the Armbian base image — Stage 3 must check and add it if needed.",
        "new_str": "1. RESOLVED (Stage 3): <code>usb_f_fs.ko</code> is present in the base image — verified by debugfs readback of the root partition (<code>/lib/modules/6.12.23-current-sunxi64/kernel/drivers/usb/gadget/function/usb_f_fs.ko</code>, <code>CONFIG_USB_FUNCTIONFS=m</code>). No kernel change needed.",
    },
    {
        "old_str": "Web app repo: <code>HomesteadLink/web-app</code> (PRD wireframes; commit to follow).",
        "new_str": "Web app repo: <code>HomesteadLink/web-app</code> (PRD wireframes, commit 3382e38).",
    },
]

args = {"allow_async": False, "page_id": DESIGN_URL, "command": "update_content",
        "content_updates": UPDATES}
cmd = ["/opt/hatch/bin/notion-cli", "call-tool", "--name", "notion-update-page",
       "--arguments-json", json.dumps(args)]
r = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
print("rc:", r.returncode)
print(r.stdout[:1500])
print(r.stderr[:500])
