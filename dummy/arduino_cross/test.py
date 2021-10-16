import serial


seri = serial.Serial('COM3', baudrate=9600, timeout=None)
print(seri.name)

a = 1

while a:
    if seri.in_waiting != 0:
        content = seri.readline()
        print(content.decode())
        # a = 0
