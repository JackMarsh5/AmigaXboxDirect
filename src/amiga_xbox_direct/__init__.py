from farm_ng.core import EventClient, EventServiceConfig

# ... inside your app initialization:
service_cfg = EventServiceConfig.from_file("service_config.json")  # load our config with canbus details
canbus_client = EventClient(service_cfg.service("canbus"))  # connect to canbus service


