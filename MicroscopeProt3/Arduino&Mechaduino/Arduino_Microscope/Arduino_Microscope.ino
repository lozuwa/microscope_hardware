#define SPEED 1000

/*---------------x driver------------------*/
#define stepsx 2
#define dirx 5
#define enx A0
#define butx 9

/*---------------y driver------------------*/
#define stepsy 3
#define diry 6
#define eny 12
#define buty 10

void setup() {
  pinMode(stepsx, OUTPUT); pinMode(dirx, OUTPUT); pinMode(enx, OUTPUT); pinMode(butx, INPUT_PULLUP);
  pinMode(stepsy, OUTPUT); pinMode(diry, OUTPUT); pinMode(eny, OUTPUT); pinMode(buty, INPUT_PULLUP);

  digitalWrite(enx , 1);
  digitalWrite(eny , 1);
  Serial.begin(115200);
  Serial.setTimeout(5);
}

void loop() {
  if (Serial.available()) {
    int x = Serial.parseInt();
    if (x == 1) {
      home_x();
      Serial.println('o');
    }
    else if (x == 2) {
      home_y();
      Serial.println('o');
    }
    else if (x == 4) {
      m_x(0);
      Serial.println('o');
    }
    else if (x == 7) {
      m_x(1);
      Serial.println('o');
    }
    else if (x == 5) {
      m_y(1);
      Serial.println('o');
    }
    else if (x == 8) {
      m_y(0);
      Serial.println('o');
    }
  }
}

//--------------- Move x --------------------

void m_x(int n) {
  /*
    n = 0 -> left
    n = 1 -> right
  */
  byte btx = digitalRead(butx);
  if (btx == 0) {
    if (n == 0) {
      digitalWrite(enx , 0);
      digitalWrite(dirx, LOW);
      for (int i = 0; i <= 5 * 16; i++) {
        digitalWrite(stepsx , LOW);
        digitalWrite(stepsx , HIGH);
        delayMicroseconds(SPEED);
      }
      digitalWrite(enx , 1);
    }
  }
  else {
    digitalWrite(enx , 0);
    if (n == 0)
      digitalWrite(dirx, LOW);
    else
      digitalWrite(dirx, HIGH);
    for (int i = 0; i <= 5 * 16; i++) {
      digitalWrite(stepsx , LOW);
      digitalWrite(stepsx , HIGH);
      delayMicroseconds(SPEED);
    }
    digitalWrite(enx , 1);
  }
}

//--------------- Move y --------------------

void m_y(int n) {
  /*
    n = 0 -> forward
    n = 1 -> back
  */
  byte bty = digitalRead(buty);
  if (bty == 0) {
    if (n == 0) {
      digitalWrite(eny, 0);
      digitalWrite(diry, HIGH);
      for (int i = 0; i <= 5 * 16; i++) {
        digitalWrite(stepsy , HIGH);
        digitalWrite(stepsy , LOW);
        delayMicroseconds(SPEED);
      }
      digitalWrite(eny, 1);
    }
  }
  else {
    digitalWrite(eny, 0);
    if (n == 0)
      digitalWrite(diry, HIGH);
    else
      digitalWrite(diry, LOW);
    for (int i = 0; i <= 5 * 16; i++) {
      digitalWrite(stepsy , HIGH);
      digitalWrite(stepsy , LOW);
      delayMicroseconds(SPEED);
    }
    digitalWrite(eny, 1);
  }
}

//--------- HOME X (2) ---------

void home_x() {
  byte btx = digitalRead(butx);
  while (btx != 0) {
    m_x(1);
    btx = digitalRead(butx);
    Serial.println(btx);
  }
  Serial.println(btx);
  for (int i = 0; i < 3; i++)
    m_x(0);
  btx = digitalRead(butx);
  while (btx != 0) {
    m_x(1);
    btx = digitalRead(butx);
  }
}

//--------- HOME Y ---------

void home_y() {
  byte bty = digitalRead(buty);
  while (bty != 0) {
    m_y(1);
    bty = digitalRead(buty);
  }
  for (int i = 0; i < 3; i++)
    m_y(0);
  bty = digitalRead(buty);
  while (bty != 0) {
    m_y(1);
    bty = digitalRead(buty);
  }
}
