/**
  Author: Khalil Nallar
  Company: pfm medical
  Description: Script that controls the logic on the microscope's hardware.
  Documentation:
  ------------
   Z axis
  ------------
  - h -> response when the home top button is pressed
  - d -> response when the autofocus top button is pressed
  - c -> response when the autofocus bottom button is pressed
  ------------
   Y axis
  ------------
  -
  ------------
   X axis
  ------------
  -
*/
#define enableY A5
#define enableX A4
#define enableZ 8
#define direccionY 5
#define direccionX 6
#define direccionZ 7
#define stepsY 2
#define stepsX 3
#define stepsZ 4
#define endY 9
#define endX 10
#define endZt A0
#define endZc A2
#define endZd A1
#define luz A3

String eje = "";
String pasos = "";
String direccion = "";
String timpo = "";
String brillo = "";
byte brillo_actual = 0;

void setup() {
  pinMode(stepsX, OUTPUT);
  pinMode(stepsY, OUTPUT);
  pinMode(stepsZ, OUTPUT);

  pinMode(direccionX, OUTPUT);
  pinMode(direccionY, OUTPUT);
  pinMode(direccionZ, OUTPUT);

  pinMode(enableY, OUTPUT);
  pinMode(enableX, OUTPUT);
  pinMode(enableZ, OUTPUT);

  pinMode(luz, OUTPUT);

  pinMode(endX, INPUT_PULLUP);
  pinMode(endY, INPUT_PULLUP);

  pinMode(endZc, INPUT);
  pinMode(endZt, INPUT);
  pinMode(endZd, INPUT);

  digitalWrite(enableZ, 1);
  digitalWrite(enableY , 1);
  digitalWrite(enableX , 1);

  Serial.begin(115200);
  Serial.setTimeout(10);
}

void loop() {
  /** Loop function */
  /** Clean serial */
  Serial.flush();
  /** Serial available */
  //Serial.println(digitalRead(endZc));
  if (Serial.available() > 0) {
    String tx = Serial.readString();
    /** Parse the strings */
    eje = tx.substring(0, tx.indexOf(","));
    tx = tx.substring(eje.length() + 1);
    pasos = tx.substring(0, tx.indexOf(","));
    tx = tx.substring(pasos.length() + 1);
    direccion = tx.substring(0, tx.indexOf(","));
    tx = tx.substring(direccion.length() + 1);
    timpo = tx.substring(0, tx.indexOf(","));
    tx = tx.substring(timpo.length() + 1);
    brillo = tx.substring(0, tx.indexOf(","));
    /** Conditions for parsing */
    if (eje == "x") {
      //Serial.println("moviendo eje x, " + pasos +" pasos, en direccion " + direccion + ",en " + timpo +" milisegundos por paso");
      x(pasos.toInt(), direccion.toInt(), timpo.toInt());
    }
    else if (eje == "y") {
      //Serial.println("moviendo eje y, " + pasos +" pasos, en direccion " + direccion + ",en " + timpo +" milisegundos por paso");
      y(pasos.toInt(), direccion.toInt(), timpo.toInt());
    }
    else if (eje == "z") {
      //Serial.print("moviendo eje z, " + pasos +" pasos, en direccion " + direccion + ",en " + timpo +" milisegundos por paso");
      z(pasos.toInt(), direccion.toInt(), timpo.toInt());
    }
    else if (eje == "homeX") {
      homeX();
    }
    else if (eje == "homeY") {
      homeY();
    }
    else if (brillo.toInt() != brillo_actual) {
      enableLed(brillo.toInt());
      brillo_actual = brillo.toInt();
    }
    else {
      return;
    }
  }
  else {
    //continue;
  }
}

void enableLed(int brillo) {
  /** Function that controls the led state
    :param brillow: input int that defines the led state
  */
  digitalWrite(luz, brillo);
}

int t = 0;
int d = 0;
void z(int pasos, int direccion, int timpo) {
  bool movementState = false;
  digitalWrite(direccionZ,direccion);
  digitalWrite(enableZ, 0);
  for (int i = 0; i < pasos; i++) {
    if (digitalRead(endZt) == 1 and direccion == 1) {
      Serial.write("d");
      movementState = true;
      t++;
      break;
    }
    else if (digitalRead(endZd) == 1 and direccion == 0) {
      Serial.write("c");
      movementState = true;
      d++;
      break;
    }
    else{
      digitalWrite(stepsZ, 1);
      delayMicroseconds(timpo);
      digitalWrite(stepsZ, 0);
      delayMicroseconds(timpo);
    }
  }
  if (movementState == false) {
    Serial.write("o");
    t = 0;
    d = 0;
  }
  else if (movementState == true and (t == 1 or d == 1)) {
    for (int i = 0; i < 50; i++) {
      digitalWrite(stepsZ, 1);
      delayMicroseconds(timpo);
      digitalWrite(stepsZ, 0);
      delayMicroseconds(timpo);
    }
  }
  //digitalWrite(enableZ, 1);
}

void y(int pasos, int direccion, int timpo) {
  /** Function that controls the movement of the motor in the Y axis
    :param pasos: input int that defines the number of steps
    :param direccion: input int that defines the direction to move
    :param timpo: input int that defines the amount of delay in
                  microseconds for each movement of the motor
  */
  /** Set direction and enable motor */
  digitalWrite(enableY, 0);
  digitalWrite(direccionY, direccion);
  for (int i = 0; i < pasos; i++) {
    /** If the endstop is pressed */
    if (direccion == 1 && digitalRead(endY) == 0) {
      break;
    }
    /** If momevement is allowed */
    else {
      digitalWrite(stepsY, 1);
      delayMicroseconds(timpo);
      digitalWrite(stepsY, 0);
      delayMicroseconds(timpo);
    }
  }
  /** Disable motor */
  digitalWrite(enableY , 1);
  /** Response */
  Serial.write("o");
}

void x(int pasos, int direccion, int timpo) {
  /** Function that controls the movement of the motor in the X axis
    :param pasos: input int that defines the number of steps
    :param direccion: input int that defines the direction to move
    :param timpo: input int that defines the amount of delay in
                  microseconds for each movement of the motor
  */
  /** Set direction and enable motor */
  //Serial.println(digitalRead(endX));
  digitalWrite(enableX, 0);
  digitalWrite(direccionX, direccion);
  for (int i = 0; i < pasos; i++) {
    /** If the motor has reached the endstop */
    if (direccion == 1 && digitalRead(endX) == 0) {
      break;
    }
    /** If movement is allowed */
    else {
      digitalWrite(stepsX, 1);
      delayMicroseconds(timpo);
      digitalWrite(stepsX, 0);
      delayMicroseconds(timpo);
    }
  }
  /** Disable motor */
  digitalWrite(enableX , 1);
  /** Response */
  Serial.write("o");
}

void homeX() {
  int timpo = 500;
  /** Enable motor */
  digitalWrite(enableX, 0);
  digitalWrite(direccionX, 1);
  while(true){
    if (digitalRead(endX) == 0) {
      break;
    }
    else {
      digitalWrite(stepsX, 1);
      delayMicroseconds(timpo);
      digitalWrite(stepsX, 0);
      delayMicroseconds(timpo);
    }
  }
  /** Disable motor */
  digitalWrite(enableX , 1);
  /** Response */
  Serial.write("o"); 
}

void homeY() {
  int timpo = 500;
  /** Set direction and enable motor */
  digitalWrite(enableY, 0);
  digitalWrite(direccionY, 1);
  while (true) {
    /** If the endstop is pressed */
    if (digitalRead(endY) == 0) {
      break;
    }
    /** If momevement is allowed */
    else {
      digitalWrite(stepsY, 1);
      delayMicroseconds(timpo);
      digitalWrite(stepsY, 0);
      delayMicroseconds(timpo);
    }
  }
  /** Disable motor */
  digitalWrite(enableY , 1);
  /** Response */
  Serial.write("o");
}