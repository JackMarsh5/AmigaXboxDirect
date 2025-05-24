# ... inside your app initialization:
service_cfg = EventServiceConfig.from_file("config.json")  # load our config with canbus details
canbus_client = EventClient(service_cfg.service("canbus"))  # connect to canbus service
from .event_client import EventClient, EventServiceConfig

