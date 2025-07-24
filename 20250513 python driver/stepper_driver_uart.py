import time
import pigpio
import serial
from typing import Type
from MCP_driver import MCP

class Stepper:
    def __init__(self, ID, mcp: Type[MCP]):
        self.ID = ID
        self.pin_EN = -1
        self.pin_MS1 = -1
        self.pin_MS2 = -1
        self.pin_DIR = -1
        self.microstep = -1
        self.SPR = 200
        self.RPM = 0
        self.status = 1
        self.mcp = mcp
        self.uart_addr = '/dev/ttyS0'
        self.init_uart()
        print(f"Stepper_driver: finished init. stepper{self.ID}")

    def config(self, pin_EN, pin_MS1, pin_MS2, pin_DIR, microstep):
        self.pin_EN = pin_EN
        self.pin_MS1 = pin_MS1
        self.pin_MS2 = pin_MS2
        self.pin_DIR = pin_DIR
        self.microstep = microstep

        for pin in [self.pin_EN, self.pin_MS1, self.pin_MS2, self.pin_DIR]:
            self.mcp.set_mode(pin, 'output')
        self.mcp.output(self.pin_EN, 1)

        if self.microstep == 8:
            self.mcp.output(self.pin_MS2, 0)
            self.mcp.output(self.pin_MS1, 0)
        elif self.microstep == 16:
            self.mcp.output(self.pin_MS2, 1)
            self.mcp.output(self.pin_MS1, 1)
        elif self.microstep == 32:
            self.mcp.output(self.pin_MS2, 0)
            self.mcp.output(self.pin_MS1, 1)
        elif self.microstep == 64:
            self.mcp.output(self.pin_MS2, 1)
            self.mcp.output(self.pin_MS1, 0)

    def init_uart(self):
        self.uart = serial.Serial(self.uart_addr, 9600, parity=serial.PARITY_NONE, timeout=0)
        t_start = time.time()
        while time.time() - t_start < 2:
            self.uart.write(f'start,{self.ID},\n'.encode())
            time.sleep(0.1)
            reply = self.uart.readline().decode('utf-8').strip()
            if reply.startswith(f"started,{self.ID}"):
                print(f"stepper_driver: UART handshake OK for stepper{self.ID}")
                break
        else:
            print(f"stepper_driver: UART timeout on stepper{self.ID}")

    def set_RPM(self, rpm):
        self.RPM = rpm
        if rpm == 0:
            self.mcp.output(self.pin_EN, 1)
            freq = 10
            duty = 0
            self.mcp.output(self.pin_DIR, 1)
        else:
            self.mcp.output(self.pin_EN, 0)
            freq = abs(int(rpm / 60 * self.SPR * self.microstep))
            duty = 30000
            self.mcp.output(self.pin_DIR, 1 if rpm > 0 else 0)

        cmd = f'set,{self.ID},{freq},{duty},{rpm}\n'
        self.uart.write(cmd.encode())

    def off(self):
        self.mcp.output(self.pin_EN, 1)
    
        

# ----- MAIN TEST ROUTINE -----
if __name__ == "__main__":
    mcp = MCP('MCP23017', 0x20)  # change address here if needed
    
    # config(self, pin_EN, pin_MS1, pin_MS2, pin_DIR, microstep)
    step0 = Stepper(0, mcp)
    step0.config(4, 5, 6, 7, 16)
    step0.set_RPM(0)

    step1 = Stepper(1, mcp)
    step1.config(3, 2, 1, 0, 16)
    step1.set_RPM(0)

    step2 = Stepper(2, mcp)
    step2.config(15, 14, 13, 12, 16)
    step2.set_RPM(0)
    
    step3 = Stepper(3, mcp)
    step3.config(8, 9, 10, 11, 16)
    step3.set_RPM(0)


    for rpm in range(-300, 300, 50):
        step0.set_RPM(rpm)
        print(f'step0 RPM:{rpm}')
        time.sleep(0.5)
    step0.set_RPM(0)

    for rpm in range(-300, 300, 50):
        step1.set_RPM(rpm)
        print(f'step0 RPM:{rpm}')
        time.sleep(0.5)
    step1.set_RPM(0)

    for rpm in range(-200, 300, 50):
        step2.set_RPM(rpm)
        print(f'step1 RPM:{rpm}')
        time.sleep(0.5)
    step2.set_RPM(0)
    
    for rpm in range(-200, 300, 50):
        step3.set_RPM(rpm)
        print(f'step1 RPM:{rpm}')
        time.sleep(0.5)
    step3.set_RPM(0)

    step0.off()
    step1.off()
    step2.off()
    step3.off()
