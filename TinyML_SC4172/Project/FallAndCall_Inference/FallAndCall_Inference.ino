/*
  FallAndCall_Inference.ino (v2.0 - Verified Detection)
  Integrated 2-Stage Emergency System with Multi-Sensor Gating
*/

#include <Arduino_LSM9DS1.h>
#include <PDM.h>
#include <TensorFlowLite.h>
#include "emergency_model.h" // Your exported TFLite model header

// System State Machine
enum State {IDLE, VERIFYING, LISTENING, ALARM};
State currentState = IDLE;

// Thresholds
const float IMPACT_THRESHOLD = 4.5; 
const float TILT_THRESHOLD_ANGLE = 60.0; // Degrees change required
const unsigned long VERIFICATION_DELAY = 1500; // Wait for person to settle

// Initial Orientation (Standing)
float standX, standY, standZ;
unsigned long stateStartTime = 0;

void setup() {
  Serial.begin(115200);
  while (!Serial);

  if (!IMU.begin()) { Serial.println("Failed to start IMU!"); while (1); }
  PDM.begin(1, 16000);
  
  // Calibration: Capture standing orientation (Assumes device starts vertical)
  Serial.println("Calibrating standing orientation... Please hold board upright.");
  delay(1000);
  if (IMU.accelerationAvailable()) {
    IMU.readAcceleration(standX, standY, standZ);
    // Normalize standing vector
    float mag = sqrt(standX*standX + standY*standY + standZ*standZ);
    standX /= mag; standY /= mag; standZ /= mag;
  }

  pinMode(LED_BUILTIN, OUTPUT);
  Serial.println("System IDLE. Monitoring for impact...");
}

void loop() {
  switch (currentState) {
    case IDLE:
      checkIMU();
      break;
      
    case VERIFYING:
      if (millis() - stateStartTime > VERIFICATION_DELAY) {
        verifyFall();
      }
      break;
      
    case LISTENING:
      runVoiceInference();
      break;
      
    case ALARM:
      digitalWrite(LED_BUILTIN, HIGH);
      Serial.println("!!! EMERGENCY ALERT SENT !!!");
      delay(5000);
      digitalWrite(LED_BUILTIN, LOW);
      currentState = IDLE;
      break;
  }
}

void checkIMU() {
  float ax, ay, az;
  if (IMU.accelerationAvailable()) {
    IMU.readAcceleration(ax, ay, az);
    float aSum = sqrt(ax*ax + ay*ay + az*az);
    
    if (aSum > IMPACT_THRESHOLD) {
      Serial.println("Impact Detected! Verifying orientation...");
      currentState = VERIFYING;
      stateStartTime = millis();
    }
  }
}

void verifyFall() {
  float ax, ay, az;
  if (IMU.accelerationAvailable()) {
    IMU.readAcceleration(ax, ay, az);
    
    // 1. Normalize current vector
    float mag = sqrt(ax*ax + ay*ay + az*az);
    ax /= mag; ay /= mag; az /= mag;

    // 2. Calculate Dot Product between Standing and Current Vector
    float dot = (ax * standX) + (ay * standY) + (az * standZ);
    
    // 3. Calculate Angle in Degrees
    float angle = acos(dot) * 180.0 / PI;
    
    Serial.print("Tilt Angle: "); Serial.println(angle);

    // 4. Check if Still (mag should be close to 1.0G)
    bool isStill = (mag > 0.8 && mag < 1.2);

    if (angle > TILT_THRESHOLD_ANGLE && isStill) {
      Serial.println("Fall Verified! Listening for voice verification...");
      currentState = LISTENING;
    } else {
      Serial.println("False Alarm (No tilt/stillness). Resetting.");
      currentState = IDLE;
    }
  }
}

void runVoiceInference() {
  // Same logic as before: Record audio, MFCCs, TFLite Invoke
  // (Assuming Lab 4 logic is implemented here)
  
  Serial.println("Listening for HELP, EMERGENCY, or CANCEL...");
  delay(2000); // Simulate processing time
  
  float help_score = 0.85; // Placeholder
  
  if (help_score > 0.7) {
    currentState = ALARM;
  } else {
    Serial.println("No distress detected. Resetting.");
    currentState = IDLE;
  }
}
