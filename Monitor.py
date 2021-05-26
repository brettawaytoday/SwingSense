#!/usr/bin/python3
from influxdb import InfluxDBClient
import uuid
import serial
import datetime
import time
import csv
import os

ser = serial.Serial('/dev/serial0', 115200, timeout=5)

client = InfluxDBClient(host='localhost', port=8086)

def millisec():
	nowTime = datetime.datetime.now()
  	ms = nowTime-startTime
  	ms = int(ms.total_seconds()*1000)

timestamp = time.strftime("%H:%M:%S.%f")  
startTime = datetime.datetime.now()

csvfile = open('/home/pi/templog.csv','a')
csvwriter = csv.writer(csvfile,delimiter=',')

while True:

	nowTime = datetime.datetime.now()

	input = ser.read_until()
	sub_input = input.decode("utf-8").split(",")

	x = sub_input[0]
	y = sub_input[1]
	z = sub_input[2]
  light = sub_input[3]

	date_s = (nowTime.strftime('%Y-%m-%d'))
	time_s = (nowTime.strftime('%H:%M:%S'))
	ms_s = (nowTime.strftime('%f'))

  line = "swing,sensor=swing001 x={},y={},z={},light={}".format(x, y, z, light)
  client.write([line], {'db': 'swingsense'}, 204, 'line')

	csvwriter.writerow([date_s,time_s,ms_s,x,y,z,light])
