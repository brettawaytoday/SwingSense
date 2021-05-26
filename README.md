# SwingSense

_Demo project using a Raspberry Pi Pico, accelerometer and UV sensor to monitor swings at a playground._

Accelerometer  data from the MPU6050 and UV data from the GYML8511 is processed by the Pico and transmitted over serial `uart.write("{},{},{},{},\n".format(angleX, angleY, angleZ, intensity))` to the Raspberry Pi base station.

The Pi base station then sends the data to an InfluxDB database and a CSV file.
``` python
line = "swing,sensor=swing001 x={},y={},z={},light={}".format(x, y, z, light)
client.write([line], {'db': 'swingsense'}, 204, 'line')
csvwriter.writerow([date_s,time_s,ms_s,x,y,z,light])
```


![Sensor diagram](https://github.com/brettawaytoday/SwingSense/blob/main/Sensor.png)

###### MPU6050 credit to https://github.com/danjperron/pico_mpu6050_ssd1331 

###### Data visualisation credit to Bitify http://blog.bitify.co.uk/2013/11/3d-opengl-visualisation-of-data-from.html
