import asyncio
import os
from inputs import get_gamepad
from farm_ng.core.event_client import EventClient
from farm_ng.core.event_service_pb2 import EventServiceConfig
from farm_ng.core.pose_pb2 import Pose  # or another available type
from amiga_xbox_direct import bluetooth


from fastapi import FastAPI
from farm_ng.core.event_client import EventServiceConfig, EventClient
from my_project.controller_input import run_controller_loop  # your module

def main():
    # Load gRPC service config
    config = EventServiceConfig.from_file("service_config.json")
    
    # Create canbus client
    canbus_client = EventClient(config.service("canbus"))

    # Start controller input loop (pass in the client)
    run_controller_loop(canbus_client)

if __name__ == "__main__":
    main()

app = FastAPI()


app.include_router(bluetooth.router)
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
