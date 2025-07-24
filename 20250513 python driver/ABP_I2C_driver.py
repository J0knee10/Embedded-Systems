import time
from smbus2 import SMBus, i2c_msg
import threading
import time
import os
from PyQt5.QtCore import pyqtSignal

# I2C address of the device
DEVICE_ADDRESS = 0x08  # replace with your device address

# Open the I2C bus
i2c_bus = SMBus(1)

# Status bits
STATUS_OK = 0
STATUS_COMMAND = 1
STATUS_STALE = 2
STATUS_DIAGNOSTIC = 3

# Pressure and temperature masks and shifts
PRESSURE_MASK = 0x3FFF
OUTPUT_MAX = 14745  # in counts, 90% of full scale which is 2^14 counts
OUTPUT_MIN = 1638  # in counts, 10%
PRESSURE_SHIFT = 16
TEMPERATURE_MASK = 0x7FF
TEMPERATURE_SHIFT = 5

# Pressure conversion factors
# Pressure for given sensor is in psi
PRESSURE_MIN = 0  # replace with your device's minimum pressure
PRESSURE_MAX = 30  # replace with your device's maximum pressure
PRESSURE_SCALE = (PRESSURE_MAX - PRESSURE_MIN) / (OUTPUT_MAX - OUTPUT_MIN)  # calculate from output max and min


class ABP_I2C:
    def __init__(self, ID):
        self.ID = ID
        self.address = 0x08
        self.mux_address = None
        self.mux_channel = None
        self.mux_mode = 0
        self.pressure = 0
        self.temperature = 0
        self.interval = 0.3
        self.status = 0
        self.thread = None

    '''
    Only selects one channel at a time, not toggle a channel
    Select from 0-7
    '''
    def set_mux(self, mux_address, mux_channel):
        self.mux_address = mux_address
        self.mux_channel = mux_channel
        self.mux_mode = 1
        status = self.select_mux_channel()
        print(f'ABP_I2C_driver: abp{self.ID} set_mux, address:{self.mux_address}, channel:{self.mux_channel}')
        print(f'ABP_I2C_driver: abp{self.ID} select_mux, status:{status}')
        self.mux_mode = 1
    
    def select_mux_channel(self):
        # Select the correct channel on the multiplexer
        i2c_bus.write_byte(self.mux_address, 1 << self.mux_channel)
        #print("here")
        #time.sleep(1)
        status = i2c_bus.read_byte(self.mux_address)  # Read the response to ensure the write completes
        if(status != 1 << self.mux_channel):
            print("Multiplexer channel select failed")
        else: 
            # print("mux activate ch success")
            status = status # do nothing here
        return status    
        
    # Read pressure only
    def read_two_bytes(self):

        # Select the correct channel on the multiplexer
        if self.mux_mode == 1:
            self.select_mux_channel() # comment this line if no multiplexer

        # Read two bytes from the device
        msg = i2c_msg.read(self.address, 2)
        i2c_bus.i2c_rdwr(msg)
        data = list(msg)

        # Swap the bytes
        data = data[0] << 8 | data[1]
        # Extract the status bits
        status = data >> 14

        # Check the status
        if status == STATUS_OK:
            # Extract the pressure data
            pressure_raw = (data & PRESSURE_MASK)
            # Convert the pressure to psi
            pressure = PRESSURE_MIN + (pressure_raw - OUTPUT_MIN) * PRESSURE_SCALE
            # Return the pressure
            return pressure
        elif status == STATUS_COMMAND:
            # Command mode, print error message
            print("Command mode, something is abnormal")
            return None
        elif status == STATUS_STALE:
            # Data is stale, return None
            # print("Data is stale")
            return None
        elif status == STATUS_DIAGNOSTIC:
            # Device is in diagnostic mode, print error message
            print("Check diagnostic condition")
            return None

    # Read pressure and temperature
    def read_four_bytes(self):
        # Select the correct channel on the multiplexer
        if self.mux_mode == 1:
            self.select_mux_channel() # comment this line if no multiplexer

        # Read four bytes from the device
        msg = i2c_msg.read(self.address, 4)
        # print('abp adress')
        i2c_bus.i2c_rdwr(msg)
        # print("read success")
        data = list(msg)

        # Swap endianess
        converted_data = (data[0] << 24) | (data[1] << 16) | (data[2] << 8) | data[3]

        # print data in binary form
        # print(f"Converted Data: {converted_data:032b}")

        # Extract the status bits
        status = (data[0] >> 6)

        # Check the status
        if status == STATUS_OK:
            # Extract the pressure and temperature data
            pressure_raw = (data[0] << 8 | data[1]) & PRESSURE_MASK
            temperature_raw = ((data[2] << 8) | (data[3])) >> 5

            # Convert the pressure to psi
            pressure = PRESSURE_MIN + (pressure_raw - OUTPUT_MIN) * PRESSURE_SCALE
            
            # constrain pressure to be within the range
            if(pressure > PRESSURE_MAX):
                pressure = PRESSURE_MAX
            elif(pressure < PRESSURE_MIN):
                pressure = PRESSURE_MIN
            # Convert the temperature to °C
            temperature = (temperature_raw * 200 / 2047) - 50  # Formula from datasheet
            # Return the pressure and temperature
            return pressure, temperature
        elif status == STATUS_COMMAND:
            # Command mode, print error message
            print("Command mode, something is abnormal")
            return None, None
        elif status == STATUS_STALE:
            # Data is stale, return None
            # print("Data is stale")
            return None, None
        elif status == STATUS_DIAGNOSTIC:
            # Device is in diagnostic mode, print error message
            print("Check diagnostic condition")
            return None, None
            
    def read_data(self):
        self.pressure = None
        self.temperature = None
        
        while self.pressure is None:
            self.pressure, self.temperature = self.read_four_bytes()
            # print("read data")
            if self.pressure is not None:
                self.pressure = self.pressure * 68.9475729
                self.pressure = round(self.pressure, 3)
                self.temperature = round(self.temperature, 3)
                # print(f"ABP_I2C_driver: ABP_I2C{self.ID}, P:{self.pressure} mbar, Temp:{self.temperature} °C, cycle_time:{self.cycle_time}")
                return self.pressure, self.temperature
                
if __name__ == "__main__":
    # Create a PressureSensor instance
    abp0 = ABP_I2C(0)
    print("declared")
    
    abp0.set_mux(0x77, 3)
    
    
    t0 = time.time()
    
    while time.time() - t0 < 10:
        pressure, temp = abp0.read_data()
        print(f'abp3, pressure:{pressure}, temp:{temp}, t:{round(time.time() - t0, 3)}')
        time.sleep(0.3)
