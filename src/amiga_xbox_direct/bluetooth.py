import subprocess
import re
import json
import logging
import time
from pathlib import Path
from fastapi import APIRouter, HTTPException

# Use this router reference in main.py
# from amiga_xbox_direct.bluetooth import router as bluetooth_router
router = APIRouter()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("amiga_xbox_direct.bluetooth")

@router.get("/bluetooth/status")
async def status():
    return {"status": "Bluetooth service active"}

# Use persistent file path under managed home
KNOWN_DEVICES_FILE = Path("/mnt/managed_home/farm-ng-user-jmarsh/AmigaXboxDirect/data/paired_xbox.json")

# Ensure the data directory exists
KNOWN_DEVICES_FILE.parent.mkdir(parents=True, exist_ok=True)

def run_bluetoothctl_commands(commands):
    """Run a sequence of bluetoothctl commands."""
    try:
        proc = subprocess.Popen(['bluetoothctl'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        out, err = proc.communicate('\n'.join(commands) + '\n')
        if proc.returncode != 0:
            logger.error(f"Bluetoothctl error: {err.strip()}")
        return out.strip()
    except Exception as e:
        logger.exception("Failed to run bluetoothctl commands")
        raise HTTPException(status_code=500, detail=str(e))

def scan_devices(timeout_sec=8):
    """Scan for nearby Bluetooth devices."""
    try:
        subprocess.run(["bluetoothctl", "scan", "on"], check=True)
        time.sleep(timeout_sec)
        subprocess.run(["bluetoothctl", "scan", "off"], check=True)

        output = subprocess.run(["bluetoothctl", "devices"], capture_output=True, text=True).stdout
        devices = []
        for line in output.splitlines():
            match = re.match(r"Device (\S+) (.+)", line)
            if match and "Xbox" in match.group(2):
                devices.append({"mac": match.group(1), "name": match.group(2)})
        return devices
    except subprocess.CalledProcessError as e:
        logger.error(f"Bluetooth scan error: {e}")
        raise HTTPException(status_code=500, detail="Bluetooth scanning failed")

def pair_device(mac):
    """Pair, trust, and connect to a device by MAC."""
    try:
        cmds = [f"pair {mac}", f"trust {mac}", f"connect {mac}"]
        result = run_bluetoothctl_commands(cmds)

        if "Connection successful" in result or "Connection already exists" in result:
            # Save MAC
            with open(KNOWN_DEVICES_FILE, "w") as f:
                json.dump({"mac": mac}, f)
            return True, "Paired successfully"
        return False, result
    except Exception as e:
        logger.exception("Failed to pair device")
        raise HTTPException(status_code=500, detail=str(e))

def get_known_device():
    """Get previously paired MAC if it exists."""
    try:
        if KNOWN_DEVICES_FILE.exists():
            with open(KNOWN_DEVICES_FILE) as f:
                return json.load(f).get("mac")
        return None
    except Exception as e:
        logger.exception("Failed to read known device file")
        return None
