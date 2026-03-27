/*
  Audio_Keyword_Capture.ino
  Record 1 second of audio for Keywords: "HELP", "EMERGENCY", "CANCEL"
*/

#include <PDM.h>

const int SAMPLE_RATE = 16000;
const int NUM_SAMPLES = 16000; // 1 second
short audioBuffer[NUM_SAMPLES];
volatile int samplesRead = 0;

void setup() {
  Serial.begin(115200);
  while (!Serial);

  PDM.onReceive(onPDMdata);
  if (!PDM.begin(1, SAMPLE_RATE)) {
    Serial.println("Failed to start PDM!");
    while (1);
  }
}

void loop() {
  Serial.println("Send 'r' to start 1-second recording...");
  while (Serial.read() != 'r');

  samplesRead = 0;
  Serial.println("--- RECORDING ---");
  
  while (samplesRead < NUM_SAMPLES) {
    // Wait for buffer to fill
  }

  Serial.println("--- DATA START ---");
  for (int i = 0; i < NUM_SAMPLES; i++) {
    Serial.println(audioBuffer[i]);
  }
  Serial.println("--- DATA END ---");
}

void onPDMdata() {
  int bytesAvailable = PDM.available();
  int samplesToRead = bytesAvailable / 2;

  if (samplesRead + samplesToRead <= NUM_SAMPLES) {
    PDM.read(audioBuffer + samplesRead, bytesAvailable);
    samplesRead += samplesToRead;
  }
}
