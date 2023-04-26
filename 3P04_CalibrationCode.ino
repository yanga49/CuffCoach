#include "BluetoothSerial.h"
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>

BluetoothSerial SerialBT;
  
Adafruit_BNO055 bno = Adafruit_BNO055(55);
#define BNO055_SAMPLERATE_DELAY_MS (100)
#define BUTTON_PIN 19


void setup(void) 
{
  SerialBT.begin("ESP32 Bluetooth");
  Serial.begin(9600);
  Serial.println(-5);
  pinMode(BUTTON_PIN, INPUT_PULLUP); // config GIOP19 as input pin and enable the internal pull-up resistor

  
  /* Initialise the sensor */
  if(!bno.begin())
  {
    /* There was a problem detecting the BNO055 ... check your connections */
    Serial.print("Ooops, no BNO055 detected ... Check your wiring or I2C ADDR!");
    while(1);
  }
  
  delay(1000);
    
  bno.setExtCrystalUse(true);


}

float avg = 0;

void loop() {

  int buttonState = digitalRead(BUTTON_PIN);
  imu::Vector<3> euler = bno.getVector(Adafruit_BNO055::VECTOR_EULER);
  //imu::Vector<3> accel_value = bno.getVector(Adafruit_BNO055::VECTOR_ACCELEROMETER);
  
  uint8_t system, gyro, accel, mag = 0;
  bno.getCalibration(&system, &gyro, &accel, &mag);

    // Prompt the user to calibrate the gyroscope
  if (gyro == 0) {
    Serial.println(-4);
  }

  if (gyro > 0) {
    if (buttonState == 0) {
      Serial.println(-5);

      // Calibrate in 5 seconds
      for (int i = 1; i <= 50; i++) {
        delay(100);
        Serial.println(-3);
      }

      // Take 30 calibration measurements (3 secs)
      for (int i = 0; i < 30; i++) {
        delay(100);
        imu::Vector<3> euler = bno.getVector(Adafruit_BNO055::VECTOR_EULER);
        avg += euler.z();
        Serial.println(-2);
      }

      // Calculate the average of the calibration measurements
      avg = avg / 30;
    }

    // Print angle measurement relative to calibrated base position
    else {
      float angle = euler.z() - avg;

      if (angle < 0 && angle >= -90) {
        angle = 0;
      }
      if (angle < -90) {
        angle = 360 + angle;
      }

      // Check that the user is not tilting their wrist about the y-axis
      float tilt = euler.y();
      if (tilt > 10 || tilt < -10) {
        Serial.println(-1);
      }

      Serial.println(angle);
    }
  }


  delay(BNO055_SAMPLERATE_DELAY_MS);
}