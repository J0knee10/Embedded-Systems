import subprocess
from gpiozero import LED

# IR device
IR_DEVICE = "/dev/lirc0"
IR_SIGNAL_FILE = "/home/pi/IRstuff/ir_signal.txt"

# LED on BCM 21
led = LED(21)

def receive_ir_signal():
    led.on()
    print("Receiving IR signal... point remote at Pi and press button")
    try:
        subprocess.run(["ir-ctl", "--device", IR_DEVICE, "--receive", IR_SIGNAL_FILE], check=True)
        print("Signal received and saved to:", IR_SIGNAL_FILE)
        with open(IR_SIGNAL_FILE, "r") as f:
            print("\n--- Captured Signal ---\n")
            print(f.read())
            print("\n--- End ---\n")
    except subprocess.CalledProcessError as e:
        print("Error receiving IR signal:", e)
    led.off()

def send_ir_signal():
    led.on()
    print("Sending IR signal...")
    try:
        subprocess.run(["ir-ctl", "--device", IR_DEVICE, "--send", IR_SIGNAL_FILE], check=True)
        print("Signal sent successfully!")
    except subprocess.CalledProcessError as e:
        print("Error sending IR signal:", e)
    led.off()

# Main
input("Press Enter to start receiving...")
receive_ir_signal()
input("Press Enter to send captured signal...")
send_ir_signal()
