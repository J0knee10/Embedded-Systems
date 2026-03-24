/*
  IMU_Fall_Capture.ino
  Stage 1: Training Data Collector for Fall Detection
  This script detects a "fall-like" event and prints 1 second of Accel/Gyro data.
*/

#include <Arduino_LSM9DS1.h>

const float IMPACT_THRESHOLD = 4.0; // G's
const float FREEFALL_THRESHOLD = 0.5; // G's
const int numSamples = 119; // ~1 second at 119Hz

void setup() {
  Serial.begin(115200);
  while (!Serial);

  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }
  Serial.println("aX,aY,aZ,gX,gY,gZ");
}

void loop() {
  float ax, ay, az, gx, gy, gz;

  if (IMU.accelerationAvailable()) {
    IMU.readAcceleration(ax, ay, az);
    float aSum = sqrt(ax*ax + ay*ay + az*az);

    // Look for Fall Signature: Freefall followed by Impact
    if (aSum < FREEFALL_THRESHOLD || aSum > IMPACT_THRESHOLD) {
      for (int i = 0; i < numSamples; i++) {
        if (IMU.accelerationAvailable() && IMU.gyroscopeAvailable()) {
          IMU.readAcceleration(ax, ay, az);
          IMU.readGyroscope(gx, gy, gz);
          
          Serial.print(ax, 3); Serial.print(",");
          Serial.print(ay, 3); Serial.print(",");
          Serial.print(az, 3); Serial.print(",");
          Serial.print(gx, 3); Serial.print(",");
          Serial.print(gy, 3); Serial.print(",");
          Serial.println(gz, 3);
        }
        delay(8); // Roughly 119Hz
      }
      Serial.println(); // Boundary for CSV parsing
    }
  }
}
