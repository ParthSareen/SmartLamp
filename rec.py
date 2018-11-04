import numpy as np
import cv2
import pickle
import requests
import serial
import math
import time
import json

face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainer.yml")
labels = {"person_name": 1}
with open("labels.pickle", "rb") as f:
    og_labels = pickle.load(f)
    labels = {v:k for k, v in og_labels.items()}

arduino = serial.Serial('COM19', 115200)

horizontalOffset = 0
verticalOffset = 0

def move3DPoint():
    jsonInput = open('data.json', 'r')
    decoded = json.load(jsonInput)
    if decoded['pinch'] > 0.7:
        updatePosition(-decoded['position'][0], decoded['position'][1], decoded['position'][2])


def setX(angle):
        angle = truncate(angle, 5, 175)
        command = "<x," + str(angle) + ">"
        #print(command)
        arduino.write(command.encode())

def setY(angle):
    angle = truncate(angle, 5, 175)
    command = "<y," + str(angle) + ">"
    #print(command)
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

def face():
    updatePosition(0, -1, 1)
    setLed(20)

def setLed(pwm):
    command = "<z," + str(pwm) + ">"
    #print(command)
    arduino.write(command.encode())

def resetPosition():
    updatePosition(0, 0, 1)
    setLed(255)

def testLed():
    for pwm in range(64):
        setLed(4 * pwm)

def testServo(pause):
    values = [-1, 0 ,1]



cap = cv2.VideoCapture(1)
resetPosition()
#url = "http://100.64.72.17:8080/shot.jpg"#changes almost everytime you use it

while (True):
    #capturing data frame by frame
    ret, frame = cap.read()
    #frames_resp = requests.get(url)
    #frame_arr = np.array(bytearray(frames_resp.content), dtype=np.uint8)
    #frame = cv2.imdecode(frame_arr, -1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor = 1.5, minNeighbors = 5)
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w] #(ycord_start-height, ycord_end-height)


        id, conf = recognizer.predict(roi_gray)
        #print("confidence is", conf)

        if labels[id] == "parth-sareen" and conf > 05:
            #print(id)
            #print(labels[id])
            font = cv2.FONT_HERSHEY_SIMPLEX
            name = "parth is saved"
            color = (255,255,255)
            box_color = (0, 255, 0)
            stroke = 2

            cv2.putText(frame, name, (x,y), font, 1, color, stroke, cv2.LINE_AA)
            end_cord_x = x + w
            end_cord_y = y + h
            cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), box_color, stroke)
            face()

        elif labels[id] == "parth-sareen":
            font = cv2.FONT_HERSHEY_SIMPLEX
            name = "Unsure"
            color = (255,255,255)
            box_color = (0, 0, 255)
            stroke = 2

            cv2.putText(frame, name, (x,y), font, 1, color, stroke, cv2.LINE_AA)
            end_cord_x = x + w
            end_cord_y = y + h
            cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), box_color, stroke)
            setLed(255)
            move3DPoint()





        img_item = "7.png" #creates image for testing




        cv2.imwrite(img_item, roi_color)
        #print(x,y,w,h)

        #color = (0, 0, 255) #BGR
        #stroke = 2
        #end_cord_x = x + w
        #end_cord_y = y + h
        #cv2.rectangle(frame, (x, y),(end_cord_x, end_cord_y), color, stroke)

    #display frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

#when proccesses are done executing, release VideoCapture
cap.release()
cv2.destroyAllWindows()
