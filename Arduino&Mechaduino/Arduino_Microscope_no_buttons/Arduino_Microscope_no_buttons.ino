#include <Wire.h>

#define SPEED 1000

/*---------------x driver------------------*/
#define stepsx 2
#define dirx 5
#define enx A0

/*---------------y driver------------------*/
#define stepsy 3
#define diry 6
#define eny 12

void setup() {
  /*--------------------------GPIO---------------------------------------------*/
  pinMode(stepsx, OUTPUT); pinMode(dirx, OUTPUT); pinMode(enx, OUTPUT);
  pinMode(stepsy, OUTPUT); pinMode(diry, OUTPUT); pinMode(eny, OUTPUT);

  digitalWrite(enx , 1);
  digitalWrite(eny , 1);
  /*-----------------------------------------------------------------------*/

  /*--------------------------I2C---------------------------------------------*/
  Wire.begin(0x04);
  Wire.onReceive(receiveEvent);
  Wire.onRequest(requestEvent);
  /*-----------------------------------------------------------------------*/

  /*--------------------------SERIAL---------------------------------------------*/
  Serial.begin(115200);
  Serial.setTimeout(5);
  /*-----------------------------------------------------------------------*/
}

void loop() {
  delay(15);
}

void requestEvent() {
  Wire.write(0x03);
}

void receiveEvent(int howMany) {
  while (Wire.available()) {
    byte x = Wire.read();
    Serial.print("Received x: ");
    Serial.println(x);
    if (x == 4) {
      m_x(0);
      requestEvent();
    }
    else if (x == 7) {
      m_x(1);
      requestEvent();
    }
    else if (x == 5) {
      m_y(1);
      requestEvent();
    }
    else if (x == 8) {
      m_y(0);
      requestEvent();
    }
  }
}

//--------------- Move x --------------------

void m_x(int n) {
  /*
    n = 0 -> left
    n = 1 -> right
  */
  digitalWrite(enx , 0);
  if (n == 0)
    digitalWrite(dirx, LOW);
  else
    digitalWrite(dirx, HIGH);
  for (int i = 0; i <= 8; i++) {
    digitalWrite(stepsx , LOW);
    digitalWrite(stepsx , HIGH);
    delayMicroseconds(SPEED);
  }
  digitalWrite(enx , 1);
}

//--------------- Move y --------------------

void m_y(int n) {
  /*
    n = 0 -> forward
    n = 1 -> back
  */
  digitalWrite(eny, 0);
  if (n == 0)
    digitalWrite(diry, HIGH);
  else
    digitalWrite(diry, LOW);
  for (int i = 0; i <= 8; i++) {
    digitalWrite(stepsy , HIGH);
    digitalWrite(stepsy , LOW);

  delayMicroseconds(SPEED);
  }
  digitalWrite(eny, 1);
}
