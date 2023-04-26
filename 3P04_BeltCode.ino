
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>
  
Adafruit_BNO055 bno = Adafruit_BNO055(55);
#define BNO055_SAMPLERATE_DELAY_MS (100)

void setup(void) 
{
  Serial.begin(9600);
  
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

bool calibrating = true;
float avg = 0;

void loop() {

  imu::Vector<3> euler = bno.getVector(Adafruit_BNO055::VECTOR_EULER);
  //imu::Vector<3> accel_value = bno.getVector(Adafruit_BNO055::VECTOR_ACCELEROMETER);
  
  uint8_t system, gyro, accel, mag = 0;
  bno.getCalibration(&system, &gyro, &accel, &mag);

  // Prompt the user to calibrate the gyroscope
  if (gyro == 0) {
    Serial.println(-2);
  }

  if (gyro > 0) {
      // Check that the user is not tilting their body about the y-axis
      float tilt = euler.y();
      if (tilt > 10) {
        Serial.println(1);
      } else if (tilt < -10) {
        Serial.println(-1);
      } else {
        Serial.println(0);
      }
  }

  delay(BNO055_SAMPLERATE_DELAY_MS);
}