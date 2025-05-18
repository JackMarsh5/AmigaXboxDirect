import os
import serial
from pyproj import Transformer
from farm_ng.core.event_client import EventClient
from farm_ng.core.event_service_pb2 import EventServiceConfig
from farm_ng.canbus.pose_pb2 import Pose2dStamped
from google.protobuf.timestamp_pb2 import Timestamp

class Localizer:
    def __init__(self):
        self.origin_utm = None
        self.transformer = Transformer.from_crs("epsg:4326", "epsg:32611", always_xy=True)

    def latlon_to_local(self, lat, lon):
        easting, northing = self.transformer.transform(lon, lat)
        if self.origin_utm is None:
            self.origin_utm = (easting, northing)
        return easting - self.origin_utm[0], northing - self.origin_utm[1]

def parse_gngll(nmea):
    parts = nmea.split(",")
    try:
        lat = float(parts[1][:2]) + float(parts[1][2:]) / 60.0
        if parts[2] == "S": lat *= -1
        lon = float(parts[3][:3]) + float(parts[3][3:]) / 60.0
        if parts[4] == "W": lon *= -1
        return lat, lon
    except:
        return None

def main():
    port = os.getenv("RTK_PORT", "/dev/ttyACM0")
    ser = serial.Serial(port, 115200, timeout=1)
    localizer = Localizer()
    client = EventClient(EventServiceConfig(name="track_follower", port=20101, host="localhost"))

    while True:
        line = ser.readline().decode(errors="ignore").strip()
        if "$GNGLL" in line:
            result = parse_gngll(line)
            if result:
                lat, lon = result
                x, y = localizer.latlon_to_local(lat, lon)
                ts = Timestamp()
                ts.GetCurrentTime()
                pose = Pose2dStamped(stamp=ts)
                pose.pose.x = x
                pose.pose.y = y
                pose.pose.theta = 0.0
                print(f"[SEND] X={x:.2f}, Y={y:.2f}")
                client.request_reply("/pose_local", pose)

