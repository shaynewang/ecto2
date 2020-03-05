#include <SoftwareSerial.h>

#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

// called this way, it uses the default address 0x40
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();
SoftwareSerial mySerial(10,11);
#define SERVO_FREQ 60 // Analog servos run at ~50 Hz updates


#define SERVOMIN  315 // This is the 'minimum' pulse length count (out of 4096)
#define SERVOMAX  510 // This is the 'maximum' pulse length count (out of 4096)

#define ESC_R_MIN 370 // 370 - 440 reverse
#define ESC_R_MAX 440
#define ESCNEU 450 // neutral
#define ESC_F_MIN 465
#define ESC_F_MAX 645 // 465 - 645 forward

#define BAUD 115200

enum Com {
  STEER = 1,
  SPEED = 2,
};

int in = 0;
bool trx_end = false;

void setup() {
  Serial.begin(BAUD, SERIAL_8N1);
  mySerial.begin(BAUD);

  pwm.begin();
  pwm.setPWMFreq(SERVO_FREQ);
  pwm.setPWM(0, 0, getPulseLength(0));  
  pwm.setPWM(1, 0, ESCNEU);
}

int getPulseLength(int steering){
  int pulselength = map(-steering, -100, 100, SERVOMIN, SERVOMAX);
  return pulselength;
}

int getSpeed(int throttle) {
  int tmp_speed = ESCNEU;
  if (throttle > 0) {
    tmp_speed = map(throttle, 1, 200, ESC_F_MIN, ESC_F_MAX);
  } else if (throttle < 0) {
    tmp_speed = map(throttle, -200, -1, ESC_R_MIN, ESC_R_MAX);
  }
  return tmp_speed;
}

int getMsg(int msg[]){
  int val1,val2;
  while (Serial.available()> 5) {
    Serial.find('H');
    val1 = Serial.read();
    val1 = Serial.read() + 256*val1;
    Serial.find(':');
    val2 = Serial.read();
    val2 = Serial.read() + 256*val2;
    msg[0] = val1;
    msg[1] = val2;
    return 0;
    }
  return -1;
}

void loop() {
    int msg [2]= {0,0};
    int err = getMsg(msg);
    if (!err) {
      pwm.setPWM(0, 0, getPulseLength(msg[0]));
      pwm.setPWM(1, 0, getSpeed(msg[1]));
    }
}
