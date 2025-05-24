# File: main.py
import asyncio
from inputs import get_gamepad, UnpluggedError
from farm_ng.core.event_client import EventServiceConfig, EventClient
from farm_ng.canbus.canbus_pb2 import Twist2d
from libs.joystick_utils import scale_axis, Vec2
import json
from farm_ng.core.event_client import EventServiceConfig, EventClient

with open("service_config.json", "r") as f:
    config_data = json.load(f)

for service in config_data["configs"]:
    if service["name"] == "canbus":
        service_cfg = EventServiceConfig()
        service_cfg.name = service["name"]
        service_cfg.host = service["host"]
        service_cfg.port = service["port"]
        break
else:
    raise RuntimeError("canbus service not found in config")

canbus_client = EventClient(service_cfg)

# Helper function to convert joystick pose to Twist2d
def vec2_to_twist(vec: Vec2) -> Twist2d:
    twist = Twist2d()
    twist.linear_velocity_x = vec.y
    twist.angular_velocity = -vec.x
    return twist

# Async control loop for Xbox input with reconnection loop and connection-loss failsafe
async def run_joystick_control(canbus_client):
    print("[INFO] Listening for Xbox joystick input...")

    while True:
        try:
            pose = Vec2()
            while True:
                try:
                    events = get_gamepad()
                except UnpluggedError:
                    print("[WARNING] Controller disconnected. Sending zero velocity.")
                    pose = Vec2()
                    await canbus_client.request_reply("/twist", vec2_to_twist(pose))
                    await asyncio.sleep(1)
                    continue

                for e in events:
                    if e.code == "ABS_X":
                        pose.x = scale_axis(e.state)
                    elif e.code == "ABS_Y":
                        pose.y = scale_axis(e.state)
                    elif e.code == "BTN_NORTH":
                        print("[EMERGENCY STOP]")
                        pose = Vec2()
                        await canbus_client.request_reply("/twist", vec2_to_twist(pose))
                        raise RuntimeError("Emergency stop triggered")
                    elif e.code == "BTN_EAST":
                        print("[Exit requested]")
                        raise KeyboardInterrupt

                await canbus_client.request_reply("/twist", vec2_to_twist(pose))
                await asyncio.sleep(0.05)

        except (RuntimeError, KeyboardInterrupt):
            print("[INFO] Stopped control loop. Waiting to resume...")
            await asyncio.sleep(1)
            if isinstance(RuntimeError, Exception):
                continue
            break

# Main entry point
def main():
  print("✅ main() is running")

   with open("service_config.json", "r") as f:
    config_data = json.load(f)

for service in config_data["configs"]:
    if service["name"] == "canbus":
        config = EventServiceConfig()
        config.name = service["name"]
        config.host = service["host"]
        config.port = service["port"]
        break
else:
    raise RuntimeError("canbus service not found in config")
    asyncio.run(run_joystick_control(canbus_client))

if __name__ == "__main__":
    main()
