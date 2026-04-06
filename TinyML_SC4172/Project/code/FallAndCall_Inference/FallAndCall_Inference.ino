#include <Arduino_LSM9DS1.h>
#include <PDM.h>
#include <arduinoFFT.h>
#include "fall_model.h"       // Your exported TFLite model header
#include "emergency_model.h"  // Your exported TFLite model header
#include "mel_filter_bank.h"
#include <TensorFlowLite.h>
#include <tensorflow/lite/micro/all_ops_resolver.h>
#include <tensorflow/lite/micro/micro_error_reporter.h>
#include <tensorflow/lite/micro/micro_interpreter.h>
#include <tensorflow/lite/schema/schema_generated.h>
#include <tensorflow/lite/version.h>

// Audio Parameters (Matching notebook)
#define SAMPLE_RATE 16000
#define FRAME_SIZE 512
#define HOP_LENGTH 256
#define NUM_FRAMES 61
#define NUM_MFCC 13
#define NUM_MEL_FILTERS 26
#define BUFFER_SIZE (FRAME_SIZE + (HOP_LENGTH * (NUM_FRAMES - 1)))

// Audio Buffer (Circular)
int16_t audio_buffer[BUFFER_SIZE];
volatile int bufferIndex = 0;
volatile uint32_t samplesCapturedTotal = 0;
uint32_t lastInferenceSampleCount = 0;
volatile bool isCollectingAudio = false;
#define VOICE_THRESHOLD 0.75

// Optimization Tables
float dct_matrix[NUM_MFCC][NUM_MEL_FILTERS];
float hanning_window[FRAME_SIZE];
struct MelBounds { int start; int end; } mel_bounds[NUM_MEL_FILTERS];

// FFT Setup
ArduinoFFT<float> FFT;
float fftReal[FRAME_SIZE];
float fftImag[FRAME_SIZE];

// global variables used for TensorFlow Lite (Micro)
tflite::MicroErrorReporter tflErrorReporter;
tflite::AllOpsResolver tflOpsResolver;

const tflite::Model* tflFallModel = nullptr;
tflite::MicroInterpreter* tflFallInterpreter = nullptr;
TfLiteTensor* tflFallInputTensor = nullptr;
TfLiteTensor* tflFallOutputTensor = nullptr;

const tflite::Model* tflEmerModel = nullptr;
tflite::MicroInterpreter* tflEmerInterpreter = nullptr;
TfLiteTensor* tflEmerInputTensor = nullptr;
TfLiteTensor* tflEmerOutputTensor = nullptr;

constexpr int arenaSize = 80 * 1024; 
byte tensorArena[arenaSize] __attribute__((aligned(16)));

enum State { IDLE, VERIFYING, LISTENING, ALARM };
State currentState = IDLE;

// fall variables
const float IMPACT_THRESHOLD = 4.5;
const float TILT_THRESHOLD_ANGLE = 60.0;
const float FALL_CONF_THRESHOLD = 0.6;
const unsigned long VERIFICATION_DELAY = 1500;
#define SAMPLES 120
float imuBuffer[SAMPLES][6];
int imuSampleIndex = 0;
int postImpactSamplesLeft = 0;

float standX, standY, standZ;
unsigned long stateStartTime = 0;
unsigned long voiceListenStartTime = 0;

const int LED_VERIFY = 8;
const int LED_LOOP = 2;
const int LED_LISTEN = 10;
const int LED_ALARM = 12;

void onPDMdata() {
  int bytesAvailable = PDM.available();
  if (bytesAvailable > 0) {
    int16_t pdmBuffer[bytesAvailable / 2];
    int samplesRead = PDM.read(pdmBuffer, bytesAvailable) / 2;

    if (isCollectingAudio) {
      for (int i = 0; i < samplesRead; i++) {
        audio_buffer[bufferIndex] = pdmBuffer[i];
        bufferIndex = (bufferIndex + 1) % BUFFER_SIZE;
        samplesCapturedTotal++;
      }
    }
  }
}

void setup() {
  Serial.begin(115200);
  while (!Serial);

  if (!IMU.begin()) {
    Serial.println("Failed to start IMU!");
    while (1);
  }

  PDM.onReceive(onPDMdata);
  if (!PDM.begin(1, 16000)) {
    Serial.println("Failed to start PDM!");
    while (1);
  }
  PDM.setGain(20);

  // Pre-calculations for speed
  for (int i = 0; i < NUM_MFCC; i++) {
    float scale = (i == 0) ? sqrt(1.0f / NUM_MEL_FILTERS) : sqrt(2.0f / NUM_MEL_FILTERS);
    for (int j = 0; j < NUM_MEL_FILTERS; j++) {
      dct_matrix[i][j] = scale * cos(M_PI * i * (2 * j + 1) / (2 * NUM_MEL_FILTERS));
    }
  }
  for (int i = 0; i < FRAME_SIZE; i++) {
    hanning_window[i] = 0.5f * (1 - cos(2 * M_PI * i / (FRAME_SIZE - 1)));
  }
  for (int f = 0; f < NUM_MEL_FILTERS; f++) {
    int start = -1, end = -1;
    for (int b = 0; b <= FRAME_SIZE / 2; b++) {
      if (mel_filter_bank[f][b] > 0) {
        if (start == -1) start = b;
        end = b;
      }
    }
    mel_bounds[f] = {start, end};
  }

  pinMode(LED_VERIFY, OUTPUT); pinMode(LED_LOOP, OUTPUT);
  pinMode(LED_LISTEN, OUTPUT); pinMode(LED_ALARM, OUTPUT);

  tflFallModel = tflite::GetModel(fall_model);
  tflEmerModel = tflite::GetModel(emergency_model);
  tflFallInterpreter = new tflite::MicroInterpreter(tflFallModel, tflOpsResolver, tensorArena, arenaSize, &tflErrorReporter);
  tflEmerInterpreter = new tflite::MicroInterpreter(tflEmerModel, tflOpsResolver, tensorArena, arenaSize, &tflErrorReporter);
  tflFallInterpreter->AllocateTensors();
  tflEmerInterpreter->AllocateTensors();
  tflFallInputTensor = tflFallInterpreter->input(0);
  tflFallOutputTensor = tflFallInterpreter->output(0);
  tflEmerInputTensor = tflEmerInterpreter->input(0);
  tflEmerOutputTensor = tflEmerInterpreter->output(0);

  Serial.println("ML models loaded. Calibrating...");
  delay(1000);
  if (IMU.accelerationAvailable()) {
    IMU.readAcceleration(standX, standY, standZ);
    float mag = sqrt(standX * standX + standY * standY + standZ * standZ);
    standX /= mag; standY /= mag; standZ /= mag;
  }
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.println("System IDLE. Monitoring...");
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
      isCollectingAudio = false;
      checkIMU();
      break;

    case VERIFYING:
      if (postImpactSamplesLeft > 0) {
        if (IMU.accelerationAvailable() && IMU.gyroscopeAvailable()) {
          IMU.readAcceleration(imuBuffer[imuSampleIndex][0], imuBuffer[imuSampleIndex][1], imuBuffer[imuSampleIndex][2]);
          IMU.readGyroscope(imuBuffer[imuSampleIndex][3], imuBuffer[imuSampleIndex][4], imuBuffer[imuSampleIndex][5]);
          imuSampleIndex = (imuSampleIndex + 1) % SAMPLES;
          postImpactSamplesLeft--;
        }
      } else if (millis() - stateStartTime > VERIFICATION_DELAY) {
        verifyFall();
      }
      break;

    case LISTENING:
    // Only run inference if we have collected at least BUFFER_SIZE samples
    // since we started listening.
    if (samplesCapturedTotal >= BUFFER_SIZE && 
        samplesCapturedTotal - lastInferenceSampleCount >= 8000) { //8000 == 500ms sliding window
        runVoiceInference();
        lastInferenceSampleCount = samplesCapturedTotal;
      }
      if (millis() - voiceListenStartTime > 10000) {
        Serial.println("Voice timeout.");
        currentState = IDLE;
      }
      break;

    case ALARM:
      isCollectingAudio = false;
      digitalWrite(LED_BUILTIN, HIGH);
      Serial.println("!!! EMERGENCY ALERT SENT !!!");
      delay(5000);
      digitalWrite(LED_BUILTIN, LOW);
      currentState = IDLE;
      break;
  }
}

void runVoiceInference() {
  // 1. Calculate the start point of the oldest sample in the circular buffer
  // bufferIndex currently points to where the NEXT sample will be written.
  int startIdx = bufferIndex; 

  // 2. Local Normalization (Scanning circular buffer)
  int16_t maxVal = 0;
  for (int i = 0; i < BUFFER_SIZE; i++) {
    int16_t absV = abs(audio_buffer[i]);
    if (absV > maxVal) maxVal = absV;
  }

  // 3. MFCC Extraction (Directly from circular buffer)
  for (int i = 0; i < NUM_FRAMES; i++) {
    // Windowing & FFT
    for (int n = 0; n < FRAME_SIZE; n++) {
      // Direct Indexing: (Start + FrameOffset + SampleOffset) % BUFFER_SIZE
      int sampleIdx = (startIdx + (i * HOP_LENGTH) + n) % BUFFER_SIZE;
      float sample = (float)audio_buffer[sampleIdx];
      if (maxVal > 0) sample /= (float)maxVal;
      
      fftReal[n] = sample * hanning_window[n];
      fftImag[n] = 0.0f;
    }
    FFT.compute(fftReal, fftImag, FRAME_SIZE, FFT_FORWARD);

    // Power Spectrum & Mel
    float power[FRAME_SIZE / 2 + 1];
    for (int n = 0; n <= FRAME_SIZE / 2; n++) power[n] = fftReal[n]*fftReal[n] + fftImag[n]*fftImag[n];

    float mel[NUM_MEL_FILTERS];
    for (int f = 0; f < NUM_MEL_FILTERS; f++) {
      float sum = 0;
      for (int b = mel_bounds[f].start; b <= mel_bounds[f].end; b++) sum += mel_filter_bank[f][b] * power[b];
      mel[f] = (sum > 0) ? 10 * log10(sum) : -100.0f;
    }

    // DCT
    for (int k = 0; k < NUM_MFCC; k++) {
      float val = 0;
      for (int j = 0; j < NUM_MEL_FILTERS; j++) val += mel[j] * dct_matrix[k][j];
      tflEmerInputTensor->data.f[k * NUM_FRAMES + i] = val;
    }
  }

  if (tflEmerInterpreter->Invoke() == kTfLiteOk) {
    float help = tflEmerOutputTensor->data.f[2];
    float cancel = tflEmerOutputTensor->data.f[1];
    float background = tflEmerOutputTensor->data.f[0];
    Serial.print("Help: "); Serial.print(help); Serial.print(" Cancel: "); Serial.print(cancel); Serial.print(" Background: "); Serial.println(background);

    if (help > VOICE_THRESHOLD) {
      Serial.println("VOICE: HELP DETECTED!");
      currentState = ALARM;
    } else if (cancel > VOICE_THRESHOLD) {
      Serial.println("VOICE: CANCEL DETECTED.");
      currentState = IDLE;
    }
  }
}

void checkIMU() {
  if (IMU.accelerationAvailable() && IMU.gyroscopeAvailable()) {
    IMU.readAcceleration(imuBuffer[imuSampleIndex][0], imuBuffer[imuSampleIndex][1], imuBuffer[imuSampleIndex][2]);
    IMU.readGyroscope(imuBuffer[imuSampleIndex][3], imuBuffer[imuSampleIndex][4], imuBuffer[imuSampleIndex][5]);
    float aSum = sqrt(pow(imuBuffer[imuSampleIndex][0],2) + pow(imuBuffer[imuSampleIndex][1],2) + pow(imuBuffer[imuSampleIndex][2],2));
    imuSampleIndex = (imuSampleIndex + 1) % SAMPLES; //circular buffer reset

    if (aSum > IMPACT_THRESHOLD) {
      Serial.println("Impact Detected!");
      currentState = VERIFYING;
      stateStartTime = millis();
      postImpactSamplesLeft = 80;
    }
  }
}

void verifyFall() {
  float ax, ay, az;
  if (IMU.accelerationAvailable()) {
    IMU.readAcceleration(ax, ay, az);
    float mag = sqrt(ax*ax + ay*ay + az*az);
    ax /= mag; ay /= mag; az /= mag;
    float dot = (ax * standX) + (ay * standY) + (az * standZ);
    float angle = acos(dot) * 180.0 / PI;
    Serial.print("Tilt: "); Serial.println(angle);

    if (angle > TILT_THRESHOLD_ANGLE && (mag > 0.8 && mag < 1.2)) {
      if (runFallInference() == 1) {
        Serial.println("Fall Verified! Listening...");
        currentState = LISTENING;
        voiceListenStartTime = millis();
        samplesCapturedTotal = 0; lastInferenceSampleCount = 0;
        isCollectingAudio = true;
      } else { currentState = IDLE; }
    } else { currentState = IDLE; }
  }
}

int runFallInference() {
  for (int i = 0; i < SAMPLES; i++) {
    int idx = (imuSampleIndex + i) % SAMPLES; //Follow chronological order
    tflFallInputTensor->data.f[i * 6 + 0] = (imuBuffer[idx][0]+3.0)/6.0;
    tflFallInputTensor->data.f[i * 6 + 1] = (imuBuffer[idx][1]+3.0)/6.0;
    tflFallInputTensor->data.f[i * 6 + 2] = (imuBuffer[idx][2]+3.0)/6.0;
    tflFallInputTensor->data.f[i * 6 + 3] = (imuBuffer[idx][3]+400.0)/800.0;
    tflFallInputTensor->data.f[i * 6 + 4] = (imuBuffer[idx][4]+400.0)/800.0;
    tflFallInputTensor->data.f[i * 6 + 5] = (imuBuffer[idx][5]+400.0)/800.0;
  }
  if (tflFallInterpreter->Invoke() != kTfLiteOk) return -1;
  return (tflFallOutputTensor->data.f[0] > FALL_CONF_THRESHOLD) ? 1 : 0;
}

void updateLEDs() {
  digitalWrite(LED_VERIFY, currentState == VERIFYING);
  digitalWrite(LED_LISTEN, currentState == LISTENING);
  digitalWrite(LED_ALARM, currentState == ALARM);
}