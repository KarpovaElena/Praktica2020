import argparse
from datetime import datetime, timedelta
import time

from influxdb import InfluxDBClient

parser = argparse.ArgumentParser()
parser.add_argument("-a", action="store", dest="ad", default="localhost", help="database address")
parser.add_argument("-n", action="store", dest="db", default="p1", help="database name")
parser.add_argument("-m", action="store", dest="mes", default="ms", help="measure name")
arg = parser.parse_args()
query = "SELECT "

print("Whats args to select? Set empty if all, else smth like: a, b, c")
t = input()
if t == "":
    query += "* "
else:
    query += t + " "
query += "FROM " + arg.mes
go_next = True
print("From what time u want to show format hour:minute:second:day:month:year(full)")
print("If not needed set empty")
t = input()
where_set = True
if t == "":
    where_set = False
else:
    date = datetime.strptime(t, "%X:%d:%m:%Y")
    dt = int(((date - datetime(1970, 1, 1)) / timedelta(microseconds=1)) * 1000)
    query += " WHERE \"time\" > " + str(dt)

print("Choose last period u want to show format hour:minute:second:day:month:year(full)")
print("If not needed set empty")
t = input()
if t != "":
    if not where_set:
        query += " WHERE "
    else:
        query += " AND "
    date = datetime.strptime(t, "%X:%d:%m:%Y")
    dt = int(((date - datetime(1970, 1, 1)) / timedelta(microseconds=1)) * 1000)
    query += "\"time\" < " + str(dt)

times = time.time()
cli = InfluxDBClient(arg.ad, database=arg.db)
qr = cli.query(query, epoch="ms")
print(time.time() - times, "seconds db request")
print(list(qr.get_points()))
