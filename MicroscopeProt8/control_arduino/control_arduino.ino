/**
* Author: Khalil Nallar
* Company: pfm medical
* Description: Script that controls the logic on the microscope's hardware. 
* Documentation:
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
#define enableX A5
#define enableY A4
#define enableZ 8
#define direccionX 5
#define direccionY 6
#define direccionZ 7
#define stepsX 2
#define stepsY 3
#define stepsZ 4
#define endX 9
#define endY 10
#define endZt A0
#define endZc A1
#define endZd A2
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
    //Serial.println(digitalRead(endX));
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
    * :param brillow: input int that defines the led state
    */
    digitalWrite(luz, brillo);
}

void z(int pasos, int direccion, int timpo) {
    /** Function that controls the movement of the motor in the Y axis
    * :param pasos: input int that defines the number of steps
    * :param direccion: input int that defines the direction to move
    * :param timpo: input int that defines the amount of delay in 
    *               microseconds for each movement of the motor
    */
    /** Variables */
    bool movementState = false;
    /** Set direction and enable motor */
    digitalWrite(direccionZ, direccion);
    digitalWrite(enableZ, 0);
    for (int i = 0; i < pasos; i++) {
        /** If the home top button is pressed*/
        if (digitalRead(endZc) == 1 and direccion == 1) {
            Serial.write("h");
            movementState = true;
            break;
        }
        /** If the autofocus top button is pressed */
        else if (digitalRead(endZt) == 1 and direccion == 1) {
            Serial.write("d");
            movementState = true;
            break;
        }
        /** If the autofocus bottom button is pressed */
        else if (digitalRead(endZd) == 1 and direccion == 0) {
            Serial.write("c");
            movementState = true;
            break;
        }
        /** If movement is allowed */
        else {
            digitalWrite(stepsZ, 1);
            delayMicroseconds(timpo);
            digitalWrite(stepsZ, 0);
            delayMicroseconds(timpo);
        }
    }
    /** Response */
    if (movementState == true) {
        Serial.write("o");
    }
    else {
        //continue;
    }
    /** Disable motor */
    digitalWrite(enableZ, 1);
}

void y(int pasos, int direccion, int timpo) {
    /** Function that controls the movement of the motor in the Y axis
    * :param pasos: input int that defines the number of steps
    * :param direccion: input int that defines the direction to move
    * :param timpo: input int that defines the amount of delay in 
    *               microseconds for each movement of the motor
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
}

void x(int pasos, int direccion, int timpo) {
    /** Function that controls the movement of the motor in the X axis
    * :param pasos: input int that defines the number of steps
    * :param direccion: input int that defines the direction to move
    * :param timpo: input int that defines the amount of delay in 
    *               microseconds for each movement of the motor
    */
    /** Set direction and enable motor */
    //Serial.println(digitalRead(endX));
    digitalWrite(enableX, 0);
    digitalWrite(direccionX, direccion);
    for (int i = 0; i < pasos; i++) {
        /** If the motor has reached the endstop */
        if (direccion == 0 && digitalRead(endX) == 0) {
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
}
