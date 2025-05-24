from farm_ng.core.event_client import EventClientConfig, EventClient
event_client_config = EventClientConfig.from_file("service_config.json")
canbus_client = EventClient(event_client_config.service("canbus"))
