#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

#define SERVOMIN  150 // This is the 'minimum' pulse length count (out of 4096)
#define SERVOMAX  520 // This is the 'maximum' pulse length count (out of 4096)
#define SERVO_FREQ 50 // Analog servos run at ~50 Hz updates

uint8_t servoPin[] = {0, 1, 2, 3, 4, 5, 6}; // in order of spine, right hip, right knee, right ankle, left hip, left knee, left ankle

int servoPos[] = {350, 355, 450, 340, 340, 220, 345};
int servoPosZero[] = {350, 355, 450, 340, 340, 220, 345};

int ledPin = 11; //For debugging

int stance = 0; //Robot's current position, 0 = standing, 1 = right foot forward, 2 = left foot forward
int m = 5; //Quasi-simultanious movement factor
int n = 0; //Number of steps taken

void setup() {
  Serial.begin(9600);

  pwm.begin();
  
  pwm.setOscillatorFrequency(27000000);  // The int.osc. is closer to 27MHz  
  pwm.setPWMFreq(SERVO_FREQ);  // Analog servos run at ~50 Hz updates

  pinMode(ledPin, OUTPUT);

  delay(10);
}

void loop() {
  flash();
  straighten();
  move(2,1);
  delay(99999);
}

void servo(int servo, int angle){
  if (angle > servoPos[servo]){
    for (uint16_t pulselen = servoPos[servo]; pulselen < angle; pulselen++){
      pwm.setPWM(servoPin[servo], 0, pulselen);
    }
  }
  else if (angle < servoPos[servo]){
    for (uint16_t pulselen = servoPos[servo]; pulselen < angle; pulselen--){
      pwm.setPWM(servoPin[servo], 0 , pulselen);
    }
  }
  servoPos[servo] = angle;
}

void straighten(){
  
  for (int z = 0; z < 6; z++){
    servo(z, servoPosZero[z]);
  }
  
  stance = 0;
  flash();
  delay(2000);
}

void flash(){
  digitalWrite(ledPin, HIGH);
  delay(500);
  digitalWrite(ledPin, LOW);
  delay(500);
}

void error(){
  digitalWrite(ledPin, HIGH);
  while(1 == 1){
    delay(100);
  }
}

void move(int nSteps, int footPref){
  if (n >= nSteps){                       //Reached requested number of steps
    if (stance == 0){
    }
    else if (stance == 1){
      //Move left foot forward
      servo(0, 150);
      quasiMove(420, 440, 340, 450, 220, 420);
      delay(1000);
      quasiMove(355, 450, 340, 275, 300, 200);
      delay(500);
      straighten();
    }
    else if (stance == 2){
      //Move right foot forward
      servo(0, 520);
      quasiMove(245, 450, 275, 320, 280, 345);
      delay(1000);
      quasiMove(420, 370, 420, 340, 220, 345);
      delay(500);
      straighten();
    }
    else {
      error();
    }
    stance = 0;
    n = 0;
  }
  
  else{                         
    //more steps to be done
    if (stance == 0){ 
      //standing still
      if (footPref == 0){
        //Move left foot forward
        servo(0, 150);
        quasiMove(355, 450, 340, 275, 300, 200);
        delay(500);
        quasiMove(345, 440, 360, 310, 240, 365);
        delay(500);
        quasiMove(270, 440, 400, 300, 300, 365);
        delay(500); 
        stance = 2;
      }
      else if (footPref == 1){
        //Move right foot forward
        servo(0, 520);
        quasiMove(420, 370, 420, 340, 220, 345);
        delay(500);
        quasiMove(385, 430, 320, 360, 230, 325);
        delay(500);
        quasiMove(395, 370, 320, 440, 230, 325);
        delay(500);
        stance = 1;
        
      }        
      else{
        error();
      }
    }
    else if (stance == 1){
      //Midstride, right foot forward
      //Move left foot forward
      servo(0, 150);
      quasiMove(420, 440, 340, 450, 220, 420);
      delay(1000);
      quasiMove(355, 450, 340, 275, 300, 200);
      delay(500);
      quasiMove(345, 440, 360, 310, 240, 365);
      delay(500);
      quasiMove(270, 440, 400, 300, 300, 365);
      delay(500); 
      stance = 2;
    }
    else if (stance == 2){
      //Midstride, left foot forward
      //Move right foot forward
      servo(0, 520);
      quasiMove(245, 450, 275, 320, 280, 345);
      delay(1000);
      quasiMove(420, 370, 420, 340, 220, 345);
      delay(500);
      quasiMove(385, 430, 320, 360, 230, 325);
      delay(500);
      quasiMove(395, 370, 320, 440, 230, 325);
      delay(500);
      stance = 1;
    }
    else {
      error();
    }
    n += 1;
  }
}


void quasiMove(int rH, int rK, int rA, int lH, int lK, int lA){
  int angles[] = {rH, rK, rA, lH, lK, lA};
  int smallAngles[6];
  for (int z = 0; z < 5; z++){
    smallAngles[z] = (angles[z] - servoPos[z+1])/m;
  }
  for (int z = 1; z < m; z++){
    for (int q = 1; q < 6; q++){
      servo(q, servoPos[q] + smallAngles[q]);
    }
  }
}
