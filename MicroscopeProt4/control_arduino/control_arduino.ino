#define stepsX 2
#define direccionX 5
#define stepsZ 3
#define direccionZ 6
#define stepsY 4
#define direccionY 7
#define enable 8
#define luz 12
#define endX 11
#define endY 10
//#define endZ 9
#define enablez A0

String eje, pasos, direccion, timpo, brillo;
byte brillo_actual=0;
byte B_endStopX=0;
byte B_endStopY=0;
void setup() {
  pinMode(stepsX, OUTPUT);
  pinMode(direccionX, OUTPUT);
  pinMode(stepsY, OUTPUT);
  pinMode(direccionY, OUTPUT);
  pinMode(stepsZ, OUTPUT);
  pinMode(direccionZ, OUTPUT);

  pinMode(enable, OUTPUT);

  pinMode(luz, OUTPUT);

  pinMode(endX, INPUT_PULLUP);
  pinMode(endY, INPUT_PULLUP);

  digitalWrite(enable , 1);
  digitalWrite(direccionZ, 0);

  Serial.begin(115200);
  Serial.setTimeout(5);
}

void loop() {
  Serial.flush();
  digitalWrite(enable , 1);
  digitalWrite(direccionZ , 0);
  digitalWrite(direccionY , 0);
  digitalWrite(direccionX , 0);
  endStop();
  
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

    //Serial.println(eje);
    //Serial.println(pasos);
    //Serial.println(direccion);
    //Serial.println(brillo);
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
    else if(brillo.toInt()!=brillo_actual){
      brillo_(brillo.toInt());
      brillo_actual=brillo.toInt();
      //Serial.println("ok");
    }
  }
}
void brillo_(int brillo){
  analogWrite(luz,brillo);
}
void z(int pasos, int direccion, int timpo) {
  digitalWrite(direccionZ, direccion);
  digitalWrite(enable, 0);
  for (int i = 0; i < pasos; i++) {
    digitalWrite(stepsZ, 1);
    delayMicroseconds(timpo);
    digitalWrite(stepsZ, 0);
    delayMicroseconds(timpo);
  }
  digitalWrite(enable , 1);
}
void y(int pasos, int direccion, int timpo) {
  digitalWrite(enable, 0);
  digitalWrite(direccionY, direccion);
  for (int i = 0; i < pasos; i++) {
    digitalWrite(stepsY, 1);
    delayMicroseconds(timpo);
    digitalWrite(stepsY, 0);
    delayMicroseconds(timpo);
  }
  digitalWrite(enable , 1);
}
void x(int pasos, int direccion, int timpo) {
  digitalWrite(enable, 0);
  digitalWrite(direccionX, direccion);
  for (int i = 0; i < pasos; i++) {
    digitalWrite(stepsX, 1);
    delayMicroseconds(timpo);
    digitalWrite(stepsX, 0);
    delayMicroseconds(timpo);
  }
  digitalWrite(enable , 1);
}
void endStop(){
  if(digitalRead(endX)==0 and B_endStopX==0){
    B_endStopX=1;
    Serial.println("x");
    delay(10);
  }
  else if(digitalRead(endX)==1 and B_endStopX==1){
    B_endStopX=0;
    delay(10);
  }
  if(digitalRead(endY)==0 and B_endStopY==0){
    B_endStopY=1;
    Serial.println("y");
    delay(1);
  }
  else if(digitalRead(endY)==1 and B_endStopY==1){
    B_endStopY=0;
    delay(1);
  }
}

