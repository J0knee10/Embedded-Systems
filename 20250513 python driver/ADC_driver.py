import ADS1x15
import time
import threading
import pigpio
from PyQt5.QtCore import pyqtSignal

class ADC():
    cycle_time_signal = pyqtSignal(int, str)
    
    def __init__(self, ID, address):
        self.ID = ID
        self.address = address
        self.adc = ADS1x15.ADS1115(1, self.address) 
        self.adc.setGain(0)         # Gain 0 >> max voltage = +/- 6.144V
        self.adc.setDataRate(7)     # 4(default): 128 SPS, 5: 250 SPS, 6: 475 SPS, 7: 860 SPS 
        self.adc.setMode(1)         # 0: continuous, 1: single(default)
        self.timeout = 200/1000
        self.t_start = 0
        self.cycle_time = 0
        print(f'ADC driver: adc{self.ID} ' \
                + f'gain:{self.adc.getGain()}, ' \
                + f'max voltage:{self.adc.getMaxVoltage()}, ' \
                + f'data_rate:{self.adc.getDataRate()}, ' \
                + f'mode:{self.adc.getMode()}, ' \
                + f'timeout:{self.timeout * 1000} ms')

    def read_data(self, channel):
        repeat = 0
        self.t_start = time.time()
        self.t0 = time.time()
        while time.time() - self.t_start < self.timeout:
                self.cycle_time = round((time.time() - self.t0) * 1000, 3) 
                self.t0 = time.time()
                repeat = repeat + 1
                # t1 = round((time.time() - t0)*1000000,2)
                # print(f'ADC driver: adc{self.ID} channel{channel} read_data repeat time:{t1} us')
                # t0 = time.time()
                voltage = self.adc.toVoltage(self.adc.readADC(channel))
                if voltage > 0:
                        self.cycle_time = round((time.time() - self.t0) * 1000, 3) 
                        self.t0 = time.time()
                        # print(f'ADC driver: adc{self.ID} channel{channel} cycletime: {self.cycle_time}') 
                        return voltage
                self.cycle_time = round((time.time() - self.t0) * 1000, 3) 
                self.t0 = time.time()
                # print(f'ADC driver: adc{self.ID} channel{channel} cycletime: {self.cycle_time}')
                '''
                self.adc.requestADC(channel)
                if self.adc.isReady() :
                        value = self.adc.toVoltage(self.adc.getValue())
                        value = round(value, 4)
                        # print(f'ADC driver: adc{self.ID} channel{channel} read_data voltage:{value}, repeat{repeat}')
                        return value
                # else:
                        # print(f'ADC driver: adc{self.ID} channel{channel} read_data failed, repeat{repeat}')
                '''
        
        print(f'ADC driver: adc{self.ID} channel{channel} read_data aborted after timeout {self.timeout*1000} ms, return -1')
        return -1
    
# driver test code
if __name__ == "__main__":
        ADC_address1 = 0x48
        ADC_address2 = 0x49
        ADC_address3 = 0x4A
        ADC_address4 = 0x4B
        
        adc1 = ADC(1, ADC_address1)
        adc2 = ADC(2, ADC_address2)
        adc3 = ADC(3, ADC_address3)
        adc4 = ADC(4, ADC_address4)
        t1 = time.time()
        t0 = time.time()
        while time.time() - t1 < 3:
                data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                for i in range(4):
                        data[i] = round(adc1.read_data(i),2)
                        data[i+4] = round(adc2.read_data(i),2)
                        data[i+8] = round(adc3.read_data(i),2)
                        data[i+12] = round(adc4.read_data(i),2)
                # print(f'{data},t:{round(time.time() - t0, 1)}')
                print(f'{data}, time: {round(time.time()- t0,2)}')
                t0 = time.time()
                # time.sleep(1)

        print(f'adc1 cycle time {adc1.cycle_time} ms')
        print(f'adc2 cycle time {adc2.cycle_time} ms')
        print(f'adc3 cycle time {adc3.cycle_time} ms')
        print(f'adc4 cycle time {adc4.cycle_time} ms')
