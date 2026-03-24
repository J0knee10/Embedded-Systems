/*
  FallAndCall_Inference.ino
  Integrated 2-Stage Emergency System
*/

#include <Arduino_LSM9DS1.h>
#include <PDM.h>
#include <TensorFlowLite.h>
#include "emergency_model.h" // Your exported TFLite model header

// TFLite Variables (Simplified for clarity)
tflite::ErrorReporter* error_reporter = nullptr;
const tflite::Model* model = nullptr;
tflite::MicroInterpreter* interpreter = nullptr;
TfLiteTensor* input = nullptr;

// Stage 1: IMU Constants
const float IMPACT_THRESHOLD = 4.5; 
const float TILT_THRESHOLD = 0.8; // Z-axis change

// System State
enum State {IDLE, LISTENING, ALARM};
State currentState = IDLE;

void setup() {
  Serial.begin(115200);
  IMU.begin();
  PDM.begin(1, 16000);
  
  // Initialize TFLite model here...
  // (Setup code identical to Lab 4 setup)
  
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  switch (currentState) {
    case IDLE:
      checkIMU();
      break;
    case LISTENING:
      runVoiceInference();
      break;
    case ALARM:
      digitalWrite(LED_BUILTIN, HIGH);
      Serial.println("!!! EMERGENCY ALERT SENT !!!");
      delay(5000);
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
      Serial.println("Fall Detected! Listening for voice verification...");
      currentState = LISTENING;
    }
  }
}

void runVoiceInference() {
  // 1. Record 1s of audio to buffer
  // 2. Compute MFCCs (identical to Lab 4 logic)
  // 3. interpreter->Invoke()
  
  // Pseudo-logic for classification:
  float help_score = 0.85; // Placeholder for model output
  
  if (help_score > 0.7) {
    currentState = ALARM;
  } else {
    Serial.println("No distress word detected. Resetting.");
    currentState = IDLE;
  }
}
