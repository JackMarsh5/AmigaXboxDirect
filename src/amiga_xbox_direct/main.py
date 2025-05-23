import asyncio
from inputs import get_gamepad
from farm_ng.core.event_client import EventServiceConfig, EventClient
from farm_ng.amiga.v1.canbus_pb2 import Twist2d
from libs.joystick_utils import scale_axis, Vec2

# Helper function to convert joystick pose to Twist2d
def vec2_to_twist(vec: Vec2) -> Twist2d:
    twist = Twist2d()
    twist.linear_velocity_x = vec.y
    twist.angular_velocity = -vec.x
    return twist

# Async control loop for Xbox input
async def run_joystick_control(canbus_client):
    print("[INFO] Listening for Xbox joystick input...")
    pose = Vec2()

    while True:
        events = get_gamepad()
        for e in events:
            if e.code == "ABS_X":
                pose.x = scale_axis(e.state)
            elif e.code == "ABS_Y":
                pose.y = scale_axis(e.state)
            elif e.code == "BTN_NORTH":  # Emergency stop
                print("[EMERGENCY STOP]")
                pose = Vec2()
                await canbus_client.request_reply("/twist", vec2_to_twist(pose))
                return
            elif e.code == "BTN_EAST":  # Exit
                print("[Exit requested]")
                return

        await canbus_client.request_reply("/twist", vec2_to_twist(pose))
        await asyncio.sleep(0.05)

# Main entry point
def main():
    config = EventServiceConfig.from_file("service_config.json")
    canbus_client = EventClient(config.service("canbus"))
    asyncio.run(run_joystick_control(canbus_client))

if __name__ == "__main__":
    main()
