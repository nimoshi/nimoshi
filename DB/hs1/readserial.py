import serial
import time

device = '/dev/ttyACM0'


while True:
    time.sleep(1)
    arduino = serial.Serial(device, 9600)
    data = arduino.readline()
    a = data[0:5]
    b = data[6:11]
    print(a)
    print(b)
