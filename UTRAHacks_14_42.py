import serial
import time
import math

arduino = serial.Serial('COM23', 115200)

horizontalOffset = 0
verticalOffset = 0

def setX(angle):
    angle = truncate(angle, 0, 180)
    command = "<x," + str(angle) + ">"
    print(command)
    arduino.write(command.encode())

def setY(angle):
    angle = truncate(angle, 0, 180)
    command = "<y," + str(angle) + ">"
    print(command)
    arduino.write(command.encode())

def truncate(value, lowerBound, upperBound):
    value = max(lowerBound, value)
    value = min(value, upperBound)

    return value

def updatePosition(horizontal, vertical, depth):
    depth = min(depth, 1)
    
    xAngle = math.atan2(depth, horizontal+horizontalOffset) * 180 / math.pi
    yAngle = math.atan2(depth, (vertical+verticalOffset)) * 180 / math.pi

    setX(xAngle)
    setY(yAngle)

def updateFace(detect):
    updatePosition(0, -1, 1)
    setLed(64)

def setLed(pwm):
    command = "<z," + str(pwm) + ">"
    print(command)
    arduino.write(command.encode())

def resetPosition():
    updatePosition(0, 0, 1)

def initialize():
    resetPosition()
    setLed(255)

def testLed():
    for pwm in range(64):
        setLed(4 * pwm)

def testServo(pause):
    values = [-1, 0 ,1]
    
    for y in values:
        for x in values:
            updatePosition(x, y, 1)
            time.sleep(pause)
