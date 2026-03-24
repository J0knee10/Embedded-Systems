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
    *   **"HELP" / "EMERGENCY":** Confirms the distress; triggers the actuator (Red LED + GPIO high).
    *   **"CANCEL":** Discards the event as a false alarm; resets the system to Stage 1.
*   **Technical Edge:** This ensures the device only "listens" when a physical fall is detected, preserving privacy and power.

## Hardware Requirements
*   **Arduino Nano 33 BLE Sense**
*   **Actuator:** 1x External Bulb (via Relay/GPIO) or Onboard RGB LED.
*   **Optional:** I2C OLED Display for real-time confidence scores.

## Data & Model (TinyML Workflow)
1.  **IMU Data:** Collected using `IMU_Capture.ino` to distinguish between "Fall," "Sitting," and "Walking."
2.  **Audio Data:** MFCC features extracted from 1-second snippets of "Help," "Emergency," "Cancel," and "Background Noise."
3.  **Inference:** TensorFlow Lite Micro (TFLM) running on-device for real-time classification.

## Getting Started: Data Collection
To build this project, follow the steps below to capture your own data:

### 1. IMU (Fall) Data
*   Upload `IMU_Fall_Capture.ino` to the Arduino.
*   Run `python serial_data_collector.py --port YOUR_PORT --file fall.csv --mode imu`.
*   Perform 50-100 "fall" actions and "normal" movements.
*   The data is stored in CSV format: `ax, ay, az, gx, gy, gz`.

### 2. Audio (Keyword) Data
*   Upload `Audio_Keyword_Capture.ino`.
*   Run `python serial_data_collector.py --port YOUR_PORT --file help.txt --mode audio`.
*   The script will wait for you to press ENTER to start a 1-second recording.
*   The raw PDM numbers will be stored in text format.

## Implementation Status
- [x] Project Concept & Architecture
- [ ] IMU Fall Detection Logic (Polling)
- [ ] Audio Dataset Collection
- [ ] CNN Model Training (Jupyter Notebook)
- [ ] TFLite Deployment & Integration
