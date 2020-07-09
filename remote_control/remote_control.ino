#include "nRF24L01.h"
#include "SPI.h"
#include "RF24.h"

#include "Wire.h"
#include "Adafruit_GFX.h"
#include "Adafruit_SSD1306.h"
#define OLED_RESET 4
#define MESSAGE_SIZE 6

// Initialize OLED display
Adafruit_SSD1306 display(OLED_RESET);

// Initialize radio transceiver
RF24 radio(9, 10);
// Unique address both transceivers talk on
const uint64_t address = 0xE6E6E648E6E6;

// Joystick class
class Joy {
  public:
    Joy(int, int, int, char*);
    void getInput(uint16_t*);
    
  private:
    char* _id;
    int _SW;
    int _X;
    int _Y;
};

Joy::Joy(int SW, int X, int Y, char* id) {
  _SW = SW;
  _X = X;
  _Y = Y;
  _id = id;
  pinMode(_SW, INPUT);
  digitalWrite(_SW, HIGH);
}
  
void Joy::getInput(uint16_t* vals) {
  if(digitalRead(_SW) == 1) {
    vals[0] = 1023 - analogRead(_X);
    vals[1] = 1023 - analogRead(_Y);
  }
}

// Initialize joysticks
Joy leftJoy = Joy(3, 3, 2, "left"); // Left joystick pinout, X/Y orientation changed
Joy rightJoy = Joy(2, 1, 0, "right"); // Right joystick pinout X/Y orientation changed

unsigned long timer;
unsigned long last_success_ts;

void setup() {
  // Setup and display welcome screen
  display.begin(SSD1306_SWITCHCAPVCC, 0x3C);
  display.clearDisplay();
  display.setTextColor(WHITE);
  display.setCursor(8,8);
  display.setTextSize(0.5);
  display.println("Ecto-2 control");
  display.display();
  delay(2000);
  
  radio.begin();
  radio.openWritingPipe(address);
  radio.setPALevel(RF24_PA_LOW);
  radio.stopListening();
}

void loop() {
  uint16_t l_inputs[2];
  leftJoy.getInput(l_inputs);
  uint16_t r_inputs[2];
  rightJoy.getInput(r_inputs);

  byte command_msg[MESSAGE_SIZE];
  // Only use x-axis from left joystick and y-axis from the right joystick
  serializedCommand(l_inputs[0], r_inputs[1], command_msg); 
  // Display state
  display.clearDisplay();
  display.setCursor(0,0);
  display.print("Input: X:");
  display.print(l_inputs[0]);
  display.print(" Y:");
  display.print(r_inputs[1]);
  display.println("");
  timer = millis();
  if(sendMsg(command_msg)) {
    timer = millis() - timer;
    last_success_ts = millis();
  } else {
    display.print("idle: ");
  }
  display.print(millis() - last_success_ts);
  display.println("ms");
  display.display();
}

// Sent message over radio
int sendMsg(char* msg) {
  return radio.write(msg, MESSAGE_SIZE);
}

// Convert input values to message send over radio
void serializedCommand(uint16_t val1, uint16_t val2, byte* buf) {
  uint8_t val1_bytes[2], val2_bytes[2];

  val1_bytes[0] = val1 >> 8; // Higher 8 bits from val1
  val1_bytes[1] = val1 & 0x00FF; // Lower 8 bits from val1
  val2_bytes[0] = val2 >> 8; // Higher 8 bits from val2
  val2_bytes[1] = val2 & 0x00FF; // Lower 8 bits from val2
  buf[0] = 'H';
  buf[1] = val1_bytes[0];
  buf[2] = val1_bytes[1];
  buf[3] = ':';
  buf[4] = val2_bytes[0];
  buf[5] = val2_bytes[1];
}
