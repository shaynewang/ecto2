import time
import serial
import RPi.GPIO as GPIO
import threading
from adafruit_servokit import ServoKit

kit = ServoKit(channels=16)
kit.servo[0].angle = 104
ESC = kit.continuous_servo[1]
print("test esc")
running = False
ESC.throttle = 0

port = serial.Serial("/dev/ttyAMA0", baudrate=9600,timeout=0.5)

def heartbeat():
  while True:
    port.write(b'A')
    time.sleep(0.5)

# Start heartbeat
heartbeat = threading.Thread(target=heartbeat)
heartbeat.start()


while not running:
    throttle = float(input("throttle:"))
    print("speed ",throttle)
    if throttle < -1 or throttle >1:
        break
    ESC.throttle = throttle

while running:
    print("Center: 110, Left: 68, Right: 154.")
    angle = int(input("Angle:"))
    if angle <= 66 or angle >=156:
        print("quiting...")
        break
    kit.servo[0].angle = angle
