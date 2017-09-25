#define stepsX 2
#define stepsY 3
#define stepsZ 4
#define direccionX 5
#define direccionY 6
#define direccionZ 7
#define enableX A4
#define enableY A5
#define enableZ 8
#define endX 9
#define endY 10
#define endZc A0
#define endZd A1
#define endZt A2
#define luz A3


String eje, pasos, direccion, timpo, brillo;
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
  Serial.flush();

  //Serial.println(digitalRead(endZt));
  //Serial.println(digitalRead(endZd);
  
  if (Serial.available() > 0) {
    String tx = Serial.readString();

    eje = tx.substring(0, tx.indexOf(","));
    tx = tx.substring(eje.length() + 1);
    pasos = tx.substring(0, tx.indexOf(","));
    tx = tx.substring(pasos.length() + 1);
    direccion = tx.substring(0, tx.indexOf(","));
    tx = tx.substring(direccion.length() + 1);
    timpo = tx.substring(0, tx.indexOf(","));
    tx = tx.substring(timpo.length() + 1);
    brillo = tx.substring(0, tx.indexOf(","));

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
    else if (brillo.toInt() != brillo_actual) {
      brillo_(brillo.toInt());
      brillo_actual = brillo.toInt();
      //Serial.println("ok");
    }
    else {
      return;
    }
  }
}
void brillo_(int brillo) {
  digitalWrite(luz, brillo);
}
void z(int pasos, int direccion, int timpo) {
  digitalWrite(direccionZ, direccion);
  digitalWrite(enableZ, 0);
  for (int i = 0; i < pasos; i++) {
    digitalWrite(stepsZ, 1);
    delayMicroseconds(timpo);
    digitalWrite(stepsZ, 0);
    delayMicroseconds(timpo);
  }

  //delay(500);
  digitalWrite(enableZ, 1);
  Serial.write("o");
}
void y(int pasos, int direccion, int timpo) {
  digitalWrite(enableY, 0);
  digitalWrite(direccionY, direccion);
  for (int i = 0; i < pasos; i++) {
    digitalWrite(stepsY, 1);
    delayMicroseconds(timpo);
    digitalWrite(stepsY, 0);
    delayMicroseconds(timpo);
  }
  digitalWrite(enableY , 1);
}
void x(int pasos, int direccion, int timpo) {
  digitalWrite(enableX, 0);
  digitalWrite(direccionX, direccion);
  for (int i = 0; i < pasos; i++) {
    digitalWrite(stepsX, 1);
    delayMicroseconds(timpo);
    digitalWrite(stepsX, 0);
    delayMicroseconds(timpo);
  }
  digitalWrite(enableX , 1);
}

