from influxdb import InfluxDBClient
import constants as CS
import time
import random


if __name__ == "__main__":
    client = InfluxDBClient(host='localhost', port=8086, database="p1")
    fields = {x: random.randint(0, 100) for x in CS.VARS_LIST}
    while True:
        client.write_points([
            {
                "measurement": "Name",
                "fields": fields
           }
        ])
        for a in fields:
            fields[a] += -1 + random.randint(0, 1)*2
        time.sleep(1)
