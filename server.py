#!/usr/bin/python
import web
import smbus
import math
import serial

ser = serial.Serial('/dev/serial0', 115200, timeout=5)
 
urls = (
    '/', 'index'
)

def dist(a,b):
    return math.sqrt((a*a)+(b*b))
 
def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)
 
def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)

class index:

    def GET(self):
        input = ser.read_until()
        sub_input = input.decode("utf-8").split(",")
        
        accel_xout = int(float(sub_input[0]))
        accel_yout = int(float(sub_input[1]))
        accel_zout = int(float(sub_input[2]))

        accel_xout_scaled = accel_xout/16384.0
        accel_yout_scaled = accel_yout/16384.0
        accel_zout_scaled = accel_zout/16384.0
       
        return str(get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled))+" "+str(get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled))


if __name__ == "__main__":

    app = web.application(urls, globals())
    app.run()
