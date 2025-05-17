import asyncio
from evdev import InputDevice, categorize, ecodes, list_devices
from farm_ng.canbus.canbus_pb2 import Twist2d
from farm_ng.core.event_client import EventClient
from farm_ng.core.event_service_pb2 import EventServiceConfig
from farm_ng.core.events_file_reader import proto_from_json_file

async def run_joystick_control(config_path="/etc/farm-ng/canbus.json"):
    config = proto_from_json_file(config_path, EventServiceConfig())
    client = EventClient(config)

    devices = [InputDevice(path) for path in list_devices()]
    joystick = next((dev for dev in devices if "Xbox" in dev.name), None)
    if not joystick:
        print("No Xbox controller found.")
        return

    print(f"Using joystick: {joystick.name}")

    twist = Twist2d()

    async for event in joystick.async_read_loop():
        if event.type == ecodes.EV_ABS:
            if event.code == ecodes.ABS_X:
                twist.angular_velocity = -event.value / 32768 * 0.5
            elif event.code == ecodes.ABS_Y:
                twist.linear_velocity_x = -event.value / 32768 * 0.5
        elif event.type == ecodes.EV_KEY:
            if event.code == ecodes.BTN_B and event.value == 1:
                print("B button pressed: exiting.")
                break
            elif event.code == ecodes.BTN_X and event.value == 1:
                print("X button pressed: emergency stop.")
                twist.linear_velocity_x = 0
                twist.angular_velocity = 0

        await client.request_reply("/twist", twist)

if __name__ == "__main__":
    asyncio.run(run_joystick_control())

