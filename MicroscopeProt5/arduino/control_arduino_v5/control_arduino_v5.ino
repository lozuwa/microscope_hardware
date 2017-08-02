#define stepsX 2
#define direccionX 5
#define stepsZ 3
#define direccionZ 6
#define stepsY 4
#define direccionY 7
#define enable 8
#define luz 12
#define endX 9
#define endY 10
#define endZ 11
#define endZtop A1
#define enablez A0

//y,1000,1,500
//x,1000,1,500

String eje, pasos, direccion, timpo, brillo;
byte brillo_actual = 0;

byte B_homeX = 1;
byte B_homeY = 1;
byte B_homeZ = 1;

void setup() {
  pinMode(stepsX, OUTPUT);
  pinMode(direccionX, OUTPUT);
  pinMode(stepsY, OUTPUT);
  pinMode(direccionY, OUTPUT);
  pinMode(stepsZ, OUTPUT);
  pinMode(direccionZ, OUTPUT);

  pinMode(enable, OUTPUT);
  pinMode(enablez, OUTPUT);

  pinMode(luz, OUTPUT);

  pinMode(endX, INPUT_PULLUP);
  pinMode(endY, INPUT_PULLUP);
  pinMode(endZ, INPUT_PULLUP);
  pinMode(endZtop, INPUT_PULLUP);

  digitalWrite(enablez, 1);
  digitalWrite(enable , 1);
  digitalWrite(direccionZ, 0);

  Serial.begin(115200);
  Serial.setTimeout(10);
}

void loop() {
  Serial.flush();
  digitalWrite(enable , 1);
  digitalWrite(direccionZ , 0);
  digitalWrite(direccionY , 0);
  digitalWrite(direccionX , 0);

  if (Serial.available() > 0) {
    String tx = Serial.readString();
    //Serial.println(tx);

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
    else if (eje == "homeX") {
      homeX();
    }
    else if (eje == "homeY") {
      homeY();
    }
    else if (eje == "homeZ") {
      homeZ();
    }
    else if (brillo.toInt() != brillo_actual) {
      brillo_(brillo.toInt());
      brillo_actual = brillo.toInt();
      //Serial.println("ok");
    }
  }
}
void brillo_(bool brillo) {
  digitalWrite(luz, brillo);
}
void z(int pasos, int direccion, int timpo) {
  digitalWrite(direccionZ, direccion);
  digitalWrite(enablez, 0);
  for (int i = 0; i < pasos; i++) {
    //Serial.println(digitalRead(endZtop));
    if(direccion == 1 and digitalRead(endZtop)==0){
      Serial.write("ok");
      break;
    }
    move_(stepsZ,timpo);
  }
  digitalWrite(enablez, 1);
  B_homeZ = 1;
}
void y(int pasos, int direccion, int timpo) {
  digitalWrite(enable, 0);
  digitalWrite(direccionY, direccion);
  for (int i = 0; i < pasos; i++) {
    move_(stepsY,timpo);
  }
  digitalWrite(enable , 1);
  B_homeY = 1;
}
void x(int pasos, int direccion, int timpo) {
  digitalWrite(enable, 0);
  digitalWrite(direccionX, direccion);
  for (int i = 0; i < pasos; i++) {
    move_(stepsX,timpo);
  }
  digitalWrite(enable , 1);
  B_homeX = 1;
}
void homeX() {
  if (B_homeX == 1) {
    digitalWrite(enable, 0);
    digitalWrite(direccionX, 0);
    while (digitalRead(endX) == 1) {
      move_(stepsX,200);
    }
    B_homeX = 0;
    digitalWrite(enable, 1);
  }
  Serial.println("x");
}
void homeY() {
  if (B_homeY == 1) {
    digitalWrite(enable, 0);
    digitalWrite(direccionY, 0);
    while (digitalRead(endY) == 1) {
      move_(stepsY,200);
    }
    B_homeY = 0;
    digitalWrite(enable, 1);
  }
  Serial.println("y");
}
void homeZ() {
  if (B_homeZ == 1) {
    digitalWrite(enablez, 0);
    digitalWrite(direccionZ, 0);
    while (digitalRead(endZ) == 1) {
      move_(stepsZ,200);
    }
    B_homeZ = 0;
    digitalWrite(enablez, 1);
  }
  Serial.println("z");
}
void move_(int motor_, int timpo_) {
  digitalWrite(motor_, 1);
  delayMicroseconds(timpo_);
  digitalWrite(motor_, 0);
  delayMicroseconds(timpo_);
}
