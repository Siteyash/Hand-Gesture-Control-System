
#include <Servo.h>

#define RED_LED 3
#define GREEN_LED 4
#define BLUE_LED 5
#define BUZZER 8
#define SERVO_PIN 9

Servo myServo;

void allOff() {
  digitalWrite(RED_LED, LOW);
  digitalWrite(GREEN_LED, LOW);
  digitalWrite(BLUE_LED, LOW);
  digitalWrite(BUZZER, LOW);
  myServo.write(0);
}

void setup() {
  Serial.begin(9600);

  pinMode(RED_LED, OUTPUT);
  pinMode(GREEN_LED, OUTPUT);
  pinMode(BLUE_LED, OUTPUT);
  pinMode(BUZZER, OUTPUT);

  myServo.attach(SERVO_PIN);

  allOff();

  Serial.println("GESTURE SYSTEM READY");
}

void loop() {

  if (Serial.available() > 0) {

    char gesture = Serial.read();

    allOff();

    switch (gesture) {

      case '0':
        // Closed fist: All OFF
        break;

      case '1':
        // One finger: Red LED
        digitalWrite(RED_LED, HIGH);
        break;

      case '2':
        // Two fingers: Green LED
        digitalWrite(GREEN_LED, HIGH);
        break;

      case '3':
        // Three fingers: Blue LED
        digitalWrite(BLUE_LED, HIGH);
        break;

      case '4':
        // Four fingers: All LEDs
        digitalWrite(RED_LED, HIGH);
        digitalWrite(GREEN_LED, HIGH);
        digitalWrite(BLUE_LED, HIGH);
        break;

      case '5':
        // Open palm: Servo + Buzzer
        myServo.write(90);
        digitalWrite(BUZZER, HIGH);
        break;
    }
  }
}
