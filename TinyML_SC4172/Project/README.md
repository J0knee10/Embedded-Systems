# Fall & Call: Multimodal Emergency Detection for TinyML

## Project Overview
This project implements an intelligent, two-stage emergency detection system using the **Arduino Nano 33 BLE Sense**. By combining motion sensing (IMU) and voice recognition (Audio), the system provides a robust, power-efficient solution for detecting falls and verifying distress signals on the edge.

## System Architecture: The 2-Stage Cascade
To optimize battery life and reduce false positives, the project uses a "Sensory Gating" approach:

### Stage 1: Physical Trigger (IMU)
*   **Sensor:** LSM9DS1 (Accelerometer + Gyroscope).
*   **Logic:** A low-power polling loop monitors for a "Fall Event."
    *   **Free-fall Phase:** Total acceleration drops below 0.5G.
    *   **Impact Phase:** Total acceleration exceeds a 4.5G threshold.
    *   **Orientation Check:** Gyroscope detects a >75 degree change in orientation, followed by a period of inactivity (the victim is down).
*   **Action:** Upon detection, the system "wakes up" Stage 2.

### Stage 2: Voice Verification (Audio CNN)
*   **Sensor:** MP34DT05 PDM Microphone.
*   **Logic:** A CNN-based Keyword Spotting (KWS) model (similar to Lab 4) is activated for a 5-second window.
*   **Keywords:**
    *   **"HELP":** Confirms the distress; triggers the actuator (Red LED + GPIO high).
    *   **"CANCEL":** Discards the event as a false alarm; resets the system to Stage 1.
*   **Technical Edge:** This ensures the device only "listens" when a physical fall is detected, preserving privacy and power.

## Hardware Requirements
*   **Arduino Nano 33 BLE Sense**
*   **Actuator:** 1x External Bulb (via Relay/GPIO) or Onboard RGB LED.
*   **Optional:** I2C OLED Display for real-time confidence scores.

## Data & Model (TinyML Workflow)
1.  **IMU Data:** Collected using `IMU_Fall_Capture.ino` (which uses a circular buffer to capture the pre-impact descent) to distinguish between "Fall," "Sitting," and "Walking."
2.  **Audio Data:** MFCC features extracted from 1-second snippets of "Help," "Cancel," and "Background Noise."
3.  **Inference:** TensorFlow Lite Micro (TFLM) running on-device for real-time classification.

## Getting Started: Data Collection
To build this project, follow the steps below to capture your own data:

### 1. IMU (Fall) Data
*   Upload `IMU_Fall_Capture.ino` to the Arduino.
*   Run `python serial_data_collector.py --port YOUR_PORT --file fall.csv --mode imu`.
*   Perform 50-100 "fall" actions (the board will automatically capture 1s of data including 0.25s of pre-impact flight).
*   The data is stored in CSV format: `ax, ay, az, gx, gy, gz`.

### 2. Audio (Keyword) Data
*   Upload `Audio_Keyword_Capture.ino`.
*   Run `python serial_data_collector.py --port YOUR_PORT --file help.csv --mode audio`.
*   The script will wait for you to press ENTER to start a 1-second recording.
*   The raw PDM numbers will be stored in CSV format (one 16,000-point recording per row).

#### Audio Collection Strategy (65/35 Split)
To ensure the model works in real-world conditions, use this variety:
*   **65% Clean Base:** Record in a quiet, enclosed room. Speak clearly at various volumes (normal, shouting, out-of-breath).
*   **35% Real-World Variety:** Record with background noise (TV playing, fans/AC running, or music).
*   **Distance Variety:** Record some samples with the sensor close to your mouth and others at "waistband height" (arm's length) to simulate a real fall.
*   **The "Background" Class (CRITICAL):** Fill `background.csv` with ONLY noise (no speaking). Include 1-2 minutes of silence, TV chatter, and mechanical hums (fans). This teaches the model to ignore non-voice sounds.

## Step-by-Step Workflow

### Phase 1: IMU Fall Detection (Stage 1)
1. **Upload Collector:** Upload `IMU_Fall_Capture.ino` to your Arduino Nano 33 BLE Sense.
2. **Collect Fall Data:** Run the following and perform **~50 varied falls** (onto a soft surface!):
   ```bash
   python serial_data_collector.py --port COM3 --file fall_data.csv --mode imu
   ```
3. **Collect Normal Data:** Run the following and perform **~50 "Negative" actions** (sitting down, jumping, flat drops, walking):
   ```bash
   python serial_data_collector.py --port COM3 --file normal_data.csv --mode imu
   ```
4. **Train Model:** Open `train_fall_model.ipynb` and run all cells to generate `fall_model.tflite`.

### Phase 2: Audio Keyword Spotting (Stage 2)
1. **Upload Collector:** Upload `Audio_Keyword_Capture.ino` to your Arduino.
2. **Collect Audio Data:** Run the following for each keyword (**Aim for ~50 audio clips per class**):
   ```bash
   # For "HELP"
   python serial_data_collector.py --port COM3 --file help.csv --mode audio
   # For "CANCEL"
   python serial_data_collector.py --port COM3 --file cancel.csv --mode audio
   # For "BACKGROUND" (silence, TV noise, etc.)
   python serial_data_collector.py --port COM3 --file background.csv --mode audio
   ```
3. **Train Model:** Open `train_emergency_model.ipynb` to train your CNN and export `emergency_model.tflite`.

### Phase 3: Integrated Deployment
1. **Convert to C:** Use a tool (like `xxd`) or a Python script to convert `.tflite` files to C-header arrays.
2. **Final Upload:** Upload `FallAndCall_Inference.ino` with your trained models included.
