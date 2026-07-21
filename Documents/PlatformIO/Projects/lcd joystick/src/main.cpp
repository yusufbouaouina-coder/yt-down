#include <Arduino.h>
#define X_AXIS A0
#define Y_AXIS A1
#define BUTTON 33

void setup() {
  Serial.begin(115200);

  pinMode(BUTTON, INPUT_PULLUP);
}

void loop() {

  delay(5);

  int xValue = analogRead(X_AXIS);
  int yValue = analogRead(Y_AXIS);
  bool buttonPressed = !digitalRead(BUTTON);
  

  Serial.print(xValue);
  Serial.print(",");

  Serial.print(yValue);
  Serial.print(",");

  Serial.println(buttonPressed);


}