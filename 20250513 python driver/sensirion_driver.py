'''
Initialize one instance of class for each flow rate sensor
Set each sensor to a different I2C address individually
'''
import threading
import time
from ctypes import *
import os
from PyQt5.QtCore import pyqtSignal, QObject
import pigpio

class SLF(QObject):
    
    def __init__(self, ID, sensor_type):
        super(SLF, self).__init__()
        
        # Get the absolute path to the directory of the current script
        dir_path = os.path.dirname(os.path.realpath(__file__))
        
        # Construct the path to the sense.so file
        lib_path = os.path.join(dir_path, "sense1.so")
        # lib_path = os.path.join(dir_path, "sf06_lf_i2c.so")
        
        self.lib = CDLL(lib_path)
        self.lib.sensirion_i2c_hal_init()
        self.raw_flow = c_int16()
        self.raw_temperature = c_int16()
        self.signaling_flags = c_uint16()
        self.sensor_type = sensor_type
        self.flowrate = 0
        self.temperature = 0 
        self.bubble_flag = 0 
        # INV_FLOW_SCALE_FACTORS_SLF3S_1300F = 500
        # INV_FLOW_SCALE_FACTORS_SLF3S_0600F = 10
        
        self.ID = ID
        if self.sensor_type == '0600':
            self.flow_factor = 10
        elif self.sensor_type == '1300':
            self.flow_factor = 500

        # set default i2c addr on init and arbitrary non-zero flow factor
        self.address = 0x08
        self.status = -1
        self.interval = 100/1000        # measure every 100 ms
        self.t_start = 0
        self.cycle_time = 0
        self.thread = None
        
        self.mux_address = None
        self.mux_channel = None
        self.mux_mode = None
        
        # self.IRQn1 = 18 # GPIO 23 is used for IRQn1
        # self.IRQn2 = 23 # GPIO 24 is used for IRQn2
        # self.IRQn3 = 24 # GPIO 25 is used for IRQn3

    def change_i2c_address(self, new_address, irq_pin, old_address=0x08):
        """
        Change the I2C address of the device. 

        :param new_address: The new I2C address to set.
        :param irq_pin: The IRQn pin to use.
        :param old_address: The old I2C address. Default is 0x08.
        :return: The status of the operation. Return value 0 implys success and the internal address is set to new_address.
        """
        self.lib.sf06_lf_init(old_address) # set C driver address to old_address
        status = self.lib.sf06_lf_change_i2c_address(new_address, irq_pin)
        if status == 0: 
            self.set_address(new_address)
            print(f'sensirion_driver: sensirion{self.ID} change_i2c_address done')
        else: 
            print(f'sensirion_driver: sensirion{self.ID} change_i2c_address failed')
        return status
    
    def set_address(self, address):
        """
        Set internal variable of C driver.

        :param address: The I2C address of the sensor.
        :return: The status of the operation.
        """
        status = self.lib.sf06_lf_init(address)
        self.address = address
        return status
   
    def soft_reset(self):
        """
        Perform a soft reset on ALL connected sensors.

        :return: The status of the operation.
        """
        # enables all channels on multiplexer to reset all sensors at once
        #self.lib.sensirion_i2c_hal_write.argtypes = [c_uint8, POINTER(c_uint8), c_uint8]
        #status = self.lib.sensirion_i2c_hal_write(self.multiplexer_address, 0b11111111, 1)
        status = self.lib.sensirion_i2c_general_call_reset()
        return status

    def set_mux(self, mux_address, mux_channel):
        self.mux_address = mux_address
        self.mux_channel = mux_channel
        self.mux_mode = 1
        status = self.select_mux_channel()
        print(f'sensirion_driver: sensirion{self.ID} set_mux, address:{self.mux_address}, channel:{self.mux_channel}')
        print(f'sensirion_driver: sensirion{self.ID} select_mux, status:{status}')

    def select_mux_channel(self):
        # Select the correct channel on the multiplexer
        self.lib.sensirion_i2c_hal_write.argtypes = [c_uint8, POINTER(c_uint8), c_uint8]
        data = c_uint8(1 << self.mux_channel)
        status = self.lib.sensirion_i2c_hal_write(self.mux_address, byref(data), 1)
        return status
    
    def start_continuous_measurement(self):
        print(f'sensirion_driver: sensirion{self.ID} start_continuous_measurement clicked')
        if(self.mux_mode == 1):
            self.select_mux_channel()
        self.lib.sf06_lf_init(self.address)
        setup_status = self.lib.sf06_lf_start_h2o_continuous_measurement()
        print(f'sensirion_driver: sensirion{self.ID} start_continuous_measurement setup_status {setup_status}')
    
    def stop_continuous_measurement(self):
        print(f'sensirion_driver: sensirion{self.ID} stop_continuous_measurement clicked')
        if(self.mux_mode == 1):
            self.select_mux_channel()
        self.lib.sf06_lf_init(self.address)
        setup_status = self.lib.sf06_lf_stop_continuous_measurement()
        print(f'sensirion_driver: sensirion{self.ID} stop_continuous_measurement setup_status {setup_status}')

    def read_data(self):
        if(self.mux_mode == 1):
            self.select_mux_channel()
            
        self.lib.sf06_lf_init(self.address)
        # Set the argument types for the function
        self.lib.sf06_lf_read_measurement_data_raw.argtypes = [POINTER(c_int16), POINTER(c_int16), POINTER(c_uint16)]
        setup_status = self.lib.sf06_lf_read_measurement_data_raw(byref(self.raw_flow), byref(self.raw_temperature), byref(self.signaling_flags))
        self.flowrate = round(self.raw_flow.value/self.flow_factor, 3)
        # self.temperature = round(self.raw_temperature.value/200, 3)
        self.temperature = self.raw_temperature.value/200
        self.bubble_flag = self.signaling_flags.value
        return self.flowrate, self.temperature, self.bubble_flag
    

# driver test code
if __name__ == "__main__":
    sensirion0 = SLF(1, '0600')
    sensirion1 = SLF(2, '1300')
    sensirion2 = SLF(3, '0600')

    # reset all sensirion sensors tgt
    sensirion2.soft_reset()
    
    # enable multiplexer
    sensirion0.set_mux(0x77, 4)
    sensirion1.set_mux(0x77, 6)
    sensirion2.set_mux(0x77, 0)

    

    # IRQn pin 18, 23, 24
    '''
    if sensirion0.change_i2c_address(0x09, 23) == 0:
        print('main: sensirion0 change address done')
    else:
        print('main: sensirion0 change address failed')
    
    if sensirion1.change_i2c_address(0x0a, 24) == 0:
        print('main: sensirion1 change address done')
    else:
        print('main: sensirion1 change address failed')
    
    if sensirion1.change_i2c_address(0x0b, 18) == 0:
        print('main: sensirion1 change address done')
    else:
        print('main: sensirion1 change address failed')
        
    sensirion0.set_address(0x09)
    sensirion1.set_address(0x0a)
    sensirion2.set_address(0x0b)
    '''
    
    t0 = time.time()
    sensirion0.start_continuous_measurement()
    sensirion1.start_continuous_measurement()
    sensirion2.start_continuous_measurement()
    
    while time.time() -  t0 < 3:    
        print(f't:{round(time.time() - t0, 3)}')
        flowrate, temperature, bubble_flag = sensirion0.read_data()
        print(f'sensi1, FR:{flowrate}, temp:{temperature}, bubble:{bubble_flag}')
        
        flowrate, temperature, bubble_flag = sensirion1.read_data()
        print(f'sensi2, FR:{flowrate}, temp:{temperature}, bubble:{bubble_flag}')
        
        flowrate, temperature, bubble_flag = sensirion2.read_data()
        print(f'sensi3, FR:{flowrate}, temp:{temperature}, bubble:{bubble_flag}')
        
        time.sleep(300/1000)

    sensirion0.stop_continuous_measurement()
    sensirion1.stop_continuous_measurement()
    sensirion2.stop_continuous_measurement()
    
    print('measurement ended')
