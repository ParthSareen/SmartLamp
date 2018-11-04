import serial
import time
import math
import json

comPort = "COM24"

arduino = serial.Serial(comPort, 115200)

def get3DPoint(jsonInput):
    try:
        decoded = json.loads(jsonInput)
        print(decoded)
        print("JSON parsing example: ", decoded['position'][0],
              decoded['position'][1],
              decoded['position'][2])
 
    except (ValueError, KeyError, TypeError):
        print("JSON format error")

horizontalOffset = 0
verticalOffset = 0

def setX(angle):
    angle = truncate(angle, 5, 175)
    command = "<x," + str(angle) + ">"
    arduino.write(command.encode())

def setY(angle):
    angle = truncate(angle, 5, 175)
    command = "<y," + str(angle) + ">"
    arduino.write(command.encode())

def truncate(value, lowerBound, upperBound):
    value = max(lowerBound, value)
    value = min(value, upperBound)

    return value

def updatePosition(horizontal, vertical, depth):
    depth = max(depth, 1)
    
    xAngle = math.atan2(depth, -(horizontal+horizontalOffset)) * 180 / math.pi
    yAngle = math.atan2(depth, -(vertical+verticalOffset)) * 180 / math.pi

    setX(xAngle)
    setY(yAngle)

def updateFace():
    updatePosition(0, -1, 1)
    setLed(64)

def setLed(pwm):
    command = "<z," + str(pwm) + ">"
    arduino.write(command.encode())

def reset():
    updatePosition(0, 0, 1)
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

def move3DPoint():
    jsonInput = open('data.json', 'r')
    decoded = json.load(jsonInput)
    if decoded['pinch'] > 0.7:
        updatePosition(decoded['position'][0], decoded['position'][1], decoded['position'][2])

while True:
    move3DPoint()
