#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

#include <nRF24L01.h>
#include <RF24.h>
#include <SPI.h>

// called this way, it uses the default address 0x40
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();
#define SERVO_FREQ 60 // Analog servos run at ~50 Hz updates


#define SERVOMIN  315 // This is the 'minimum' pulse length count (out of 4096)
#define SERVOMAX  510 // This is the 'maximum' pulse length count (out of 4096)

#define ESC_R_MIN 370 // 370 - 440 reverse
#define ESC_R_MAX 440
#define ESCNEU 450 // neutral
#define ESC_F_MIN 465
#define ESC_F_MAX 645 // 465 - 645 forward

#define BAUD 115200

int STEER_CH = 0; // pca9685 channel for steering(servo)
int SPEED_CH = 1; // pca9685 channel for speed(motor ESC)

RF24 radio(9, 10);
const uint64_t address = 0xE6E6E648E6E6; // Unique address both transmitter and receiver talk on

void setup() {
  Serial.begin(BAUD, SERIAL_8N1);
  
  radio.begin();
  radio.openReadingPipe(0, address);
  radio.setDataRate(RF24_250KBPS);
  radio.setPALevel(RF24_PA_MAX);
  radio.startListening();

  pwm.begin();
  pwm.setPWMFreq(SERVO_FREQ);
  pwm.setPWM(STEER_CH, 0, getSteering(0));  
  pwm.setPWM(SPEED_CH, 0, ESCNEU);
}

int getSteering(int steering){
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

// Get command from RF24 and convert steering range to (-100,100), speed range to (-200,200)
int getRadioMsg(int msg[]) {
  byte buf[6];
  if (radio.available()) {
    radio.read(buf, sizeof(buf));
    if(buf[0] == 'H' && buf[3] ==':') {
      msg[0] = -(buf[2] + buf[1]*256 - 520)/5.2;
      msg[1] = (buf[5] + buf[4]*256 - 530)/2.65;
      Serial.print("Got ");
      Serial.print(msg[0]);
      Serial.print(" ");
      Serial.print(msg[1]);
      Serial.print("\n");
      return 0;
    }
  }
  return -1;
}

// Get command from serial
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
    int err = getRadioMsg(msg);
    if (!err) {
      pwm.setPWM(STEER_CH, 0, getSteering(msg[0])); //Set steering
      pwm.setPWM(SPEED_CH, 0, getSpeed(msg[1])); //Set motor speed
    }
}
