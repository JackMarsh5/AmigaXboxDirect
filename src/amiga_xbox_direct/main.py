import asyncio
from inputs import get_gamepad
from farm_ng.core.event_client import EventServiceConfig, EventClient
from farm_ng.amiga.v1.canbus_pb2 import Twist2d  # Ensure this import is correct
from fastapi import FastAPI
from bluetooth import router as bluetooth_router

# FastAPI app setup (optional web interface)
app = FastAPI()
app.include_router(bluetooth.router)

# Helper function to scale Xbox joystick input
def scale_axis(value):
    return (value - 128) / 128.0  # Convert 0–255 to -1.0 to 1.0

# Async control loop for Xbox input
async def run_joystick_control(canbus_client):
    print("[INFO] Listening for Xbox joystick input...")
    
    while True:
        events = get_gamepad()
        msg = Twist2d()
        for e in events:
            if e.code == "ABS_X":  # Left joystick horizontal
                msg.angular_velocity = -scale_axis(e.state)
            elif e.code == "ABS_Y":  # Left joystick vertical
                msg.linear_velocity_x = scale_axis(e.state)
            elif e.code == "BTN_NORTH":  # X button (emergency stop)
                print("[EMERGENCY STOP]")
                msg.linear_velocity_x = 0.0
                msg.angular_velocity = 0.0
                await canbus_client.request_reply("/twist", msg)
                return
            elif e.code == "BTN_EAST":  # B button (exit)
                print("[Exit requested]")
                return

        await canbus_client.request_reply("/twist", msg)
        await asyncio.sleep(0.05)

# Main entry point
def main():
    config = EventServiceConfig.from_file("service_config.json")
    canbus_client = EventClient(config.service("canbus"))
    asyncio.run(run_joystick_control(canbus_client))

if __name__ == "__main__":
    main()
