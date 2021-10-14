import serial
import time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime, timedelta
import pprint
from influxdb import InfluxDBClient
from copy import deepcopy
import pytz

import datetime

#sudo chmod a+rw /dev/ttyACM0
device = 'COM4'

def get_ifdb(db, host='180.70.53.4', port=11334, user='root', passwd='root'):
	client = InfluxDBClient(host, port, user, passwd, db)
	try:
		client.create_database(db)
	except:
		pass
	return client





while True:
    try:
        arduino = serial.Serial(device, 9600)

        time.sleep(2)
        data = arduino.readline()
        a = data[0:5]
        b = data[6:11]
        print(a)
        print(b)
        try:
            write_api = client.write_api(write_options=SYNCHRONOUS)

            sequence = ["mem,host=host1 humi=a",
                "mem,host=host1 temp=b"]
            write_api.write(bucket, org, sequence)


        finally:
            client.close()
    except:
        print("")

'''

write_api = client.write_api(write_options=SYNCHRONOUS)

sequence = ["mem,host=host1 humi=90",
            "mem,host=host1 temp=20"]
write_api.write(bucket, org, sequence)
'''

query_api = client.query_api()
query = 'from(bucket:"{}")\
|> range(start: -1m)\
|> filter(fn:(r) => r._measurement == "mem")\
|> filter(fn:(r) => r._field == "usage_percent" )'.format(bucket)
result = client.query_api().query(org=org, query=query)