import asyncio
import os
from inputs import get_gamepad
from farm_ng.core.event_client import EventClient
from farm_ng.core.event_service_pb2 import EventServiceConfig
from farm_ng.canbus.canbus_pb2 import Twist2d
from farm_ng.canbus.twist_pb2 import Twist2d
from amiga_xbox_direct import bluetooth_api

from fastapi import FastAPI
from amiga_xbox_direct import bluetooth_api

app = FastAPI()
app.include_router(bluetooth_api.router)

# Optional: your websocket or other app routes here

def scale_axis(value):
    return (value - 128) / 128.0  # Convert 0–255 to -1.0 to 1.0

async def run_joystick_control():
    client = EventClient(EventServiceConfig(name="track_follower", port=20101, host="localhost"))
    print("[INFO] Listening for Xbox joystick input...")

    while True:
        events = get_gamepad()
        msg = Twist2d()
        for e in events:
            if e.code == "ABS_X":  # Left joystick horizontal
                msg.angular = -scale_axis(e.state)
            elif e.code == "ABS_Y":  # Left joystick vertical
                msg.linear = scale_axis(e.state)
            elif e.code == "BTN_NORTH":  # X button
                print("[EMERGENCY STOP]")
                msg.linear = 0
                msg.angular = 0
                await client.request_reply("/cmd_vel", msg)
                return
            elif e.code == "BTN_EAST":  # B button
                print("[Exit requested]")
                return
        await client.request_reply("/cmd_vel", msg)
        await asyncio.sleep(0.05)

def main():
    asyncio.run(run_joystick_control())
