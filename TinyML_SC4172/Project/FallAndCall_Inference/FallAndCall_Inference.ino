/*
  FallAndCall_Inference.ino (v2.0 - Verified Detection)
  Integrated 2-Stage Emergency System with Multi-Sensor Gating
*/

#include <Arduino_LSM9DS1.h>
#include <PDM.h>
#include "fall_model.h"       // Your exported TFLite model header
#include "emergency_model.h"  // Your exported TFLite model header
#include <TensorFlowLite.h>
#include <tensorflow/lite/micro/all_ops_resolver.h>
#include <tensorflow/lite/micro/micro_error_reporter.h>
#include <tensorflow/lite/micro/micro_interpreter.h>
#include <tensorflow/lite/schema/schema_generated.h>
#include <tensorflow/lite/version.h>


// global variables used for TensorFlow Lite (Micro)
tflite::MicroErrorReporter tflErrorReporter;

// pull in all the TFLM ops, you can remove this line and
// only pull in the TFLM ops you need, if would like to reduce
// the compiled size of the sketch.
tflite::AllOpsResolver tflOpsResolver;

const tflite::Model* tflFallModel = nullptr;
tflite::MicroInterpreter* tflFallInterpreter = nullptr;
TfLiteTensor* tflFallInputTensor = nullptr;
TfLiteTensor* tflFallOutputTensor = nullptr;

const tflite::Model* tflEmerModel = nullptr;
tflite::MicroInterpreter* tflEmerInterpreter = nullptr;
TfLiteTensor* tflEmerInputTensor = nullptr;
TfLiteTensor* tflEmerOutputTensor = nullptr;

// Create a static memory buffer for TFLM, the size may need to
// be adjusted based on the model you are using
constexpr int arenaSize = 32 * 1024;

byte fallArena[arenaSize] __attribute__((aligned(16)));
byte emerArena[arenaSize] __attribute__((aligned(16)));

// System State Machine
enum State { IDLE,
             VERIFYING,
             LISTENING,
             ALARM };
State currentState = IDLE;

// variables
const float IMPACT_THRESHOLD = 4.5;
const float TILT_THRESHOLD_ANGLE = 60.0;        // Degrees change required
const float FALL_CONF_THRESHOLD = 0.7;
const unsigned long VERIFICATION_DELAY = 1500;  // Wait for person to settle
#define SAMPLES 120
float imuBuffer[SAMPLES][6];
int sampleIndex = 0;

// Initial Orientation (Standing)
float standX, standY, standZ;
unsigned long stateStartTime = 0;
// LED pins
const int LED_VERIFY = 8;
const int LED_LOOP = 2;
const int LED_LISTEN = 10;
const int LED_ALARM = 12;

void setup() {
  Serial.begin(115200);
  while (!Serial)
    ;

  if (!IMU.begin()) {
    Serial.println("Failed to start IMU!");
    while (1)
      ;
  }
  PDM.begin(1, 16000);
  pinMode(LED_VERIFY, OUTPUT);
  pinMode(LED_LOOP, OUTPUT);
  pinMode(LED_LISTEN, OUTPUT);
  pinMode(LED_ALARM, OUTPUT);
  tflFallModel = tflite::GetModel(fall_model);
  tflEmerModel = tflite::GetModel(emergency_model);
  if (tflFallModel->version() != TFLITE_SCHEMA_VERSION) {
    Serial.println("Model schema mismatch!");
    while (1);
  }

  // Create an interpreter to run the model
  tflFallInterpreter = new tflite::MicroInterpreter(tflFallModel, tflOpsResolver, fallArena, arenaSize, &tflErrorReporter);
  tflEmerInterpreter = new tflite::MicroInterpreter(tflEmerModel, tflOpsResolver, emerArena, arenaSize, &tflErrorReporter);

  // Allocate memory for the model's input and output tensors
  tflFallInterpreter->AllocateTensors();
  tflEmerInterpreter->AllocateTensors();

  tflFallInputTensor = tflFallInterpreter->input(0);
  tflFallOutputTensor = tflFallInterpreter->output(0);
  tflEmerInputTensor = tflEmerInterpreter->input(0);
  tflEmerOutputTensor = tflEmerInterpreter->output(0);

  Serial.println("ML model loaded successfully!");

  // Calibration: Capture standing orientation (Assumes device starts vertical)
  Serial.println("Calibrating standing orientation... Please hold board upright.");
  delay(1000);
  if (IMU.accelerationAvailable()) {
    IMU.readAcceleration(standX, standY, standZ);
    // Normalize standing vector
    float mag = sqrt(standX * standX + standY * standY + standZ * standZ);
    standX /= mag;
    standY /= mag;
    standZ /= mag;
  }

  pinMode(LED_BUILTIN, OUTPUT);
  Serial.println("System IDLE. Monitoring for impact...");
}

void loop() {
  static unsigned long lastBlink = 0;
  if (millis() - lastBlink > 500) {
    digitalWrite(LED_LOOP, !digitalRead(LED_LOOP));
    lastBlink = millis();
  }
  updateLEDs();
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
      Serial.println("System IDLE. Monitoring for impact...");
      break;
  }
  //digitalWrite(LED_LOOP, LOW);
  //delay(1000);
}

void checkIMU() {
  float ax, ay, az;
  float gx, gy, gz;

  if (IMU.accelerationAvailable() && IMU.gyroscopeAvailable()) {

    IMU.readAcceleration(ax, ay, az);
    IMU.readGyroscope(gx, gy, gz);

    imuBuffer[sampleIndex][0] = ax;
    imuBuffer[sampleIndex][1] = ay;
    imuBuffer[sampleIndex][2] = az;

    imuBuffer[sampleIndex][3] = gx;
    imuBuffer[sampleIndex][4] = gy;
    imuBuffer[sampleIndex][5] = gz;

    sampleIndex = (sampleIndex + 1) % SAMPLES;
    float aSum = sqrt(ax * ax + ay * ay + az * az);

    if (aSum > IMPACT_THRESHOLD) {
      Serial.println("Impact Detected! Verifying orientation...");
      currentState = VERIFYING;
      stateStartTime = millis();
    }
  }
}

void verifyFall() {
  float ax, ay, az;
  int fallFlag = -1;
  if (IMU.accelerationAvailable()) {
    IMU.readAcceleration(ax, ay, az);

    // 1. Normalize current vector
    float mag = sqrt(ax * ax + ay * ay + az * az);
    ax /= mag;
    ay /= mag;
    az /= mag;

    // 2. Calculate Dot Product between Standing and Current Vector
    float dot = (ax * standX) + (ay * standY) + (az * standZ);

    // 3. Calculate Angle in Degrees
    float angle = acos(dot) * 180.0 / PI;

    Serial.print("Tilt Angle: ");
    Serial.println(angle);

    // 4. Check if Still (mag should be close to 1.0G)
    bool isStill = (mag > 0.8 && mag < 1.2);

    if (angle > TILT_THRESHOLD_ANGLE && isStill) {
      Serial.println("Orientation verified! Running ML check...");
      fallFlag = runFallInference();
      if (fallFlag == 1){
        Serial.println("Fall detected! Listening for voice verification...");
        currentState = LISTENING;
      }else if (fallFlag == 0){
        currentState = IDLE;
      }else{
        Serial.println("ML failed");
        currentState = IDLE;
      }
      
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
  delay(2000);  // Simulate processing time

  float help_score = 0.85;  // Placeholder

  if (help_score > 0.7) {
    currentState = ALARM;
  } else {
    Serial.println("No distress detected. Resetting.");
    currentState = IDLE;
  }
}

void updateLEDs() {
  digitalWrite(LED_VERIFY, LOW);
  digitalWrite(LED_LISTEN, LOW);
  digitalWrite(LED_ALARM, LOW);

  switch (currentState) {
    case IDLE:
      break;

    case VERIFYING:
      digitalWrite(LED_VERIFY, HIGH);
      break;

    case LISTENING:
      digitalWrite(LED_LISTEN, HIGH);
      break;

    case ALARM:
      digitalWrite(LED_ALARM, HIGH);
      break;
  }
}

int runFallInference() {
  Serial.print("Input size: ");
  Serial.println(tflFallInputTensor->bytes / sizeof(float));

  // 1. Copy IMU buffer into model input
  for (int i = 0; i < SAMPLES; i++) {
    tflFallInputTensor->data.f[i * 6 + 0] = (imuBuffer[i][0]+3.0)/6.0;
    tflFallInputTensor->data.f[i * 6 + 1] = (imuBuffer[i][1]+3.0)/6.0;
    tflFallInputTensor->data.f[i * 6 + 2] = (imuBuffer[i][2]+3.0)/6.0;
    tflFallInputTensor->data.f[i * 6 + 3] = (imuBuffer[i][3]+400.0)/800.0;
    tflFallInputTensor->data.f[i * 6 + 4] = (imuBuffer[i][4]+400.0)/800.0;
    tflFallInputTensor->data.f[i * 6 + 5] = (imuBuffer[i][5]+400.0)/800.0;
  }

  // 2. Run inference
  if (tflFallInterpreter->Invoke() != kTfLiteOk) {
    Serial.println("Inference failed!");
    return -1;
  }

  // 3. Read output
  float fall = tflFallOutputTensor->data.f[0];
  float normal = tflFallOutputTensor->data.f[1];

  Serial.print("Normal: ");
  Serial.println(normal);
  Serial.print("Fall: ");
  Serial.println(fall);

  // 4. Decision
  if (fall > FALL_CONF_THRESHOLD) {
    Serial.println("ML: FALL DETECTED");
    // currentState = LISTENING;
    return 1;
  } else {
    Serial.println("ML: NORMAL");
    // currentState = IDLE;
    return 0;
  }
}
