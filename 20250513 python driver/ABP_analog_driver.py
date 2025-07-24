import ADS1x15
import time
import threading
# import lgpio
import pigpio
from ADC_driver import ADC
from PyQt5.QtCore import pyqtSignal, QObject

class ABP_analog(QObject):
    # ABP_analog_readout_signal = [ID, pressure]
    ABP_analog_readout_signal = pyqtSignal(int, float)
    
    def __init__(self, ID, sensor_type, adc:type[ADC], channel):
        super(ABP_analog, self).__init__()
        self.ID = ID
        self.sensor_type = sensor_type
        self.adc = adc
        self.adc_channel = channel
        self.t_start = 0
        self.status = -1
        self.pressure = 0
        self.voltage = 0
        self.voltage_min = 0
        self.voltage_max = 5
        self.interval = 0.1     # measure every 100 ms
        self.cycle_time = 0
        self.thread = None
        
        if self.sensor_type == 'DAN':
            self.pressure_max = 2000
            self.pressure_min = 0
        elif self.sensor_type == 'DRR':
            self.pressure_max = 1000
            self.pressure_min = -1000
    
    def read_data(self): 
        self.voltage = self.adc.read_data(self.adc_channel)
        self.pressure = round(self.voltage2pressure(self.voltage),3)
        return self.pressure
            
    def voltage2pressure(self, voltage):
        voltage_diff = self.voltage_max - self.voltage_min
        pressure_diff = self.pressure_max - self.pressure_min
        pressure = (voltage - self.voltage_min) / voltage_diff * pressure_diff + self.pressure_min
        return pressure
    
    
if __name__ == "__main__":
    adc1 = ADC(1, 0x4B)
    t0 = time.time()
    
    
    print('abp testing')    
    abp1 = ABP_analog(1, 'DAN', adc1, 1)
    abp2 = ABP_analog(2, 'DRR', adc1, 2)
    t0 = time.time()
    

    while time.time() - t0 < 4:
        print(f'abp1 : {abp1.read_data()}, abp2 : {abp2.read_data()}, t: {round(time.time() - t0, 2)}')
        time.sleep(0.2)
        
    print('timeout')
    