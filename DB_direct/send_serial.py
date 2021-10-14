from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime
import time

# You can generate a Token from the "Tokens Tab" in the UI
token = "vBWv8n1gmBGfUSfvhxsSITw9xm3XsuMAs5tcLmXx4Qa-pF5AOXd_i5vjKrOV2pBc-Sgqr8uH25DAR89_uDaWVg=="
org = "12"
bucket = "12"

client = InfluxDBClient(url="http://localhost:8086", token=token)

write_api = client.write_api(write_options=SYNCHRONOUS)
for i in range(10):
    point = Point("sensor_ht")\
      .tag("host", "host1")\
      .field("humi", 50.4+i)\
      .field("temp", 30.2+i)\
      .time(datetime.utcnow(), WritePrecision.NS)

    write_api.write(bucket, org, point)
    time.sleep(1)

# sequence = ["mem,host=host1 humi=23",
#             "mem,host=host1 temp=14"]
# write_api.write(bucket, org, sequence)


query_api = client.query_api()
query = 'from(bucket:"{}")\
|> range(start: -1m)\
|> filter(fn:(r) => r._measurement == "mem")\
|> filter(fn:(r) => r._field == "usage_percent" )'.format(bucket)
result = client.query_api().query(org=org, query=query)