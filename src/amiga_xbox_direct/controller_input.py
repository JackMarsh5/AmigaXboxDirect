import evdev
from farm_ng.amiga import Twist2d  # assuming Twist2d message class is provided here

# Find the controller device by name or by available inputs
dev = None
for name in evdev.list_devices():
    d = evdev.InputDevice(name)
    if "Xbox Wireless Controller" in d.name:
        dev = d
        break
if dev is None:
    raise RuntimeError("Xbox controller not found")

# Normalize function for stick values (assuming 0-255 range -> -1.0 to 1.0)
def norm(val, center=128, span=128):
    return (val - center) / float(span)  # for X/Y axes on Xbox, center ~128

# Prepare twist message and loop
twist = Twist2d()
max_lin = 1.0  # m/s, example max linear speed
max_ang = 1.0  # rad/s, example max angular speed

for event in dev.read_loop():  # blocking loop reading controller events
    if event.type == evdev.ecodes.EV_ABS:
        absevent = evdev.util.categorize(event)  # categorize to AbsEvent
        code = evdev.ecodes.bytype[event.type][event.code]
        if code == "ABS_X":  # left stick horizontal
            x = norm(absevent.event.value) 
            twist.angular_velocity = max_ang * -x   # left = positive angular rate
        elif code == "ABS_Y":  # left stick vertical
            y = norm(absevent.event.value)
            twist.linear_velocity_x = max_lin * y   # forward = positive linear vel
        # (Add handling for other axes/triggers if needed)
        # Whenever we update twist, send it:
        canbus_client.request_reply("/twist", twist)
