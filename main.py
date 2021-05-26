import utime
import math
import mpu6050
from machine import Pin, SPI, ADC, UART
import json

#Accelerometer
mpu = mpu6050.MPU6050()
mpu.setSampleRate(500)
mpu.setGResolution(2)

counter = 0
intensity = 0.0

def averageMPU(count, timing_ms):
    gx = 0
    gy = 0
    gz = 0
    
    grx = 0
    gry = 0
    grz = 0
    
    gxoffset =  0.07
    gyoffset = -0.04
    for i in range(count):
        g = mpu.readData()
        # offset mpu
        gx = gx + g.Gx - gxoffset
        gy = gy + g.Gy - gyoffset
        gz = gz + g.Gz
        
        grx = grx + g.Gyrox
        gry = gry + g.Gyroy
        grz = grz + g.Gyroz
        
        utime.sleep_ms(timing_ms)
        
    return gx/count, gy/count, gz/count, grx/count, gry/count, grz/count

def getuv():
    global intensity
    voltage = board_v.read_u16()
    
    light = uv_out.read_u16() # 65535
    
    output = 3.3 / voltage * light

    x = output
    in_min = 0.99
    in_max = 2.8
    out_min = 0.0
    out_max = 15.0
    
    intensity = (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


#UV Sensor
board_v = ADC(28)
uv_out = ADC(26)
getuv()

#UART - Serial communication
uart = UART(1,115200)

while True:
    counter += 1
    
    if counter > 50:
        getuv()
        counter = 0

    
    gx, gy, gz, grx, gry, grz = averageMPU(20, 5)
    
    vdim = math.sqrt(gx * gx + gy * gy + gz * gz)
           
    # get angle
    rad2degree = 180 / math.pi
    angleX =  rad2degree * math.asin(gx / vdim)
    angleY =  rad2degree * math.asin(gy / vdim)
    angleZ =  rad2degree * math.asin(gz / vdim)
    
    uart.write("{},{},{},{},\n".format(angleX, angleY, angleZ, intensity))
