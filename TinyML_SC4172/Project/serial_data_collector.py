"""
serial_data_collector.py
Nano 33 BLE Sense Data Collection Tool

USAGE STEPS:
1. Identify your Arduino COM port (e.g., COM3, COM4) in the Arduino IDE.
2. Upload the corresponding .ino sketch (IMU_Fall_Capture or Audio_Keyword_Capture).
3. Close the Arduino Serial Monitor (only one program can use the port at a time).
4. Run this script from your terminal:

   FOR IMU FALL DATA:
   python serial_data_collector.py --port COM3 --file fall_data.csv --mode imu

   FOR AUDIO KEYWORD DATA:
   python serial_data_collector.py --port COM3 --file help_voice.csv --mode audio

5. In 'audio' mode, the script will wait for you to press ENTER before sending 'r' 
   to the Arduino to start a 1-second recording.
"""

import serial
import argparse
import os

def collect_data(port, baud, filename, mode):
    print(f"Opening port {port} at {baud} baud...")
    ser = serial.Serial(port, baud, timeout=1)
    
    # Clear buffer
    ser.reset_input_buffer()
    
    print(f"Mode: {mode}")
    print(f"Output: {filename}")
    print("Press Ctrl+C to stop recording.")

    with open(filename, "a") as f:
        try:
            while True:
                if mode == "audio":
                    # Clear any old "Send 'r'..." messages from the buffer
                    ser.reset_input_buffer()
                    print("\nPress Enter to trigger a 1-second recording (sending 'r')...")
                    input()
                    ser.write(b'r')
                    
                    samples = []
                    is_collecting = False
                    while True:
                        line = ser.readline().decode('utf-8').strip()
                        if "--- DATA START ---" in line:
                            print("Recording detected. Collecting...")
                            is_collecting = True
                            continue
                        if "--- DATA END ---" in line:
                            if samples:
                                f.write(",".join(samples) + "\n")
                                print(f"Finished sample ({len(samples)} points saved to CSV).")
                            break
                        if is_collecting and line:
                            samples.append(line)
                else:
                    # IMU Mode: Just append every line to the CSV
                    line = ser.readline().decode('utf-8').strip()
                    if line:
                        print(line)
                        f.write(line + "\n")
                        
        except KeyboardInterrupt:
            print("\nStopping collection...")
        finally:
            ser.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Serial Data Collector for Nano 33 BLE Sense")
    parser.add_argument("--port", type=str, required=True, help="COM port (e.g., COM3)")
    parser.add_argument("--baud", type=int, default=115200, help="Baud rate (default: 115200)")
    parser.add_argument("--file", type=str, required=True, help="Filename to save (e.g., fall_data.csv)")
    parser.add_argument("--mode", type=str, choices=["imu", "audio"], default="imu", help="Data type: imu or audio")
    
    args = parser.parse_args()
    collect_data(args.port, args.baud, args.file, args.mode)
