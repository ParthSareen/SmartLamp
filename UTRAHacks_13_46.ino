#include <Servo.h>

const int MAX_BUFFER = 256;

const int LED = 3;
const int X_SERVO_PIN = 5;
const int Y_SERVO_PIN = 6;

const int SET_X = 120;          //x
const int SET_Y = 121;          //y
const int SET_BRIGHTNESS = 122; //z

char receivedChars[MAX_BUFFER];
char tempChars[MAX_BUFFER];

Servo xServo;
Servo yServo;

boolean newData = false;

void setup() {
  Serial.begin(115200);
  pinMode(LED, OUTPUT);

  xServo.attach(X_SERVO_PIN);
  yServo.attach(Y_SERVO_PIN);
}

void loop() {
  receiveMarkers();
  if (newData) {
    strcpy(tempChars, receivedChars);
    parseData();
    newData = false;
  }
}

void receiveMarkers() {
  static boolean inProgress = false;
  static byte index = 0;
  char startMarker = '<';
  char endMarker = '>';
  char newChar;

  while (Serial.available() > 0 && newData == false) {
    newChar = Serial.read();

    if (inProgress == true) {
      if (newChar != endMarker) {
        receivedChars[index] = newChar;
        index++;
        if (index >= MAX_BUFFER) {
          index = MAX_BUFFER - 1;
        }
      }
      else {
        receivedChars[index] = '\0'; // terminate the string
        inProgress = false;
        index = 0;
        newData = true;
      }
    }

    else if (newChar == startMarker) {
      inProgress = true;
    }
  }
}

void parseData() {
  
  char * strtokIndx;
  strtokIndx = strtok(tempChars, ",");
  
  switch(tempChars[0]) {
    
    case SET_BRIGHTNESS: {
      strtokIndx = strtok(NULL, ",");
      int value = constrain(atoi(strtokIndx), 0, 255);

//      Serial.println("setting brightness to " + (String)value);
      
      analogWrite(LED, value);
    }
    break;
    
    case SET_X: {
      strtokIndx = strtok(NULL, ",");
      int value = constrain(atoi(strtokIndx), 0, 180);

//      Serial.println("setting x to " + (String)value);
      
      xServo.write(value);
    }
    break;

    case SET_Y: {
      strtokIndx = strtok(NULL, ",");
      int value = constrain(atoi(strtokIndx), 0, 180);

//      Serial.println("setting y to " + (String)value);
      
      yServo.write(value);
    }
    break;
  }
}

