import asyncio
from inputs import get_gamepad, UnpluggedError
from farm_ng.core.event_client import EventServiceConfig, EventClient
from farm_ng.amiga.v1.canbus_pb2 import Twist2d

# Helper function to scale Xbox joystick input
def scale_axis(value):
    return (value - 128) / 128.0  # Convert 0–255 to -1.0 to 1.0

# Async control loop for Xbox input with reconnection loop and connection-loss failsafe
async def run_joystick_control(canbus_client):
    print("[INFO] Listening for Xbox joystick input...")

    while True:
        try:
            pose = Twist2d()
            while True:
                try:
                    events = get_gamepad()
                except UnpluggedError:
                    print("[WARNING] Controller disconnected. Sending zero velocity.")
                    pose.linear_velocity_x = 0.0
                    pose.angular_velocity = 0.0
                    await canbus_client.request_reply("/twist", pose)
                    await asyncio.sleep(1)
                    continue

                for e in events:
                    if e.code == "ABS_X":
                        pose.angular_velocity = -scale_axis(e.state)
                    elif e.code == "ABS_Y":
                        pose.linear_velocity_x = scale_axis(e.state)
                    elif e.code == "BTN_NORTH":
                        print("[EMERGENCY STOP]")
                        pose.linear_velocity_x = 0.0
                        pose.angular_velocity = 0.0
                        await canbus_client.request_reply("/twist", pose)
                        raise RuntimeError("Emergency stop triggered")
                    elif e.code == "BTN_EAST":
                        print("[Exit requested]")
                        raise KeyboardInterrupt

                await canbus_client.request_reply("/twist", pose)
                await asyncio.sleep(0.05)

        except (RuntimeError, KeyboardInterrupt):
            print("[INFO] Stopped control loop. Waiting to resume...")
            await asyncio.sleep(1)
            if isinstance(RuntimeError, Exception):
                continue
            break

# Main entry point
def main():
    config = EventServiceConfig.from_file("service_config.json")
    canbus_client = EventClient(config.service("canbus"))
    asyncio.run(run_joystick_control(canbus_client))

if __name__ == "__main__":
    main()
