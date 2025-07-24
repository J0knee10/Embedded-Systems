from typing import Type
# from MCP_driver import MCP
from MCP_driver_PWM import MCP
import ADS1x15
import time
import threading
# import lgpio
import pigpio
from ADC_driver import ADC
from PyQt5.QtCore import pyqtSignal

class PQ12():
    cycle_time_signal = pyqtSignal(int, str)
    
    def __init__(self, mcp1: Type[MCP], mcp2: Type[MCP], mcp3: Type[MCP], adc1: Type[ADC], adc2: Type[ADC], adc3: Type[ADC]):
        self.mcp1 = mcp1
        self.mcp2 = mcp2
        self.mcp3 = mcp3
        
        self.mcp1_pinA = [0, 2, 4, 6]
        self.mcp1_pinB = [1, 3, 5, 7]
        
        self.mcp2_pinA = [0, 2, 4, 6]
        self.mcp2_pinB = [1, 3, 5, 7]
        
        self.mcp3_pinA = [0, 2, 4, 6]
        self.mcp3_pinB = [1, 3, 5, 7]
        
        self.adc1 = adc1
        self.adc2 = adc2
        self.adc3 = adc3
        
        # pq12.adc_channel_index = [3, 1, 7, 5, \
        #                11, 9, 2, 0, \
        #                 8, 10, 4, 6]

        
        self.adc_channel_index = [-1, -1, -1, -1, -1, -1, -1 ,-1, -1, -1, -1, -1] 
        
        self.voltage_current = [-1, -1, -1, -1, -1, -1, -1 ,-1, -1, -1, -1, -1] 

        self.stroke_target = [-1, -1, -1, -1, -1, -1, -1 ,-1, -1, -1, -1, -1]        
        self.stroke_current = [-1, -1, -1, -1, -1, -1, -1 ,-1, -1, -1, -1, -1] 
        self.stroke_diff = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.voltage_max = [-1,-1,-1,-1, -1,-1,-1,-1, -1,-1,-1,-1]
        self.voltage_min = [-1,-1,-1,-1, -1,-1,-1,-1, -1,-1,-1,-1]
        self.voltage_diff = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        
        self.status = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        
        self.stroke_tolerance = 0.001
        self.interval = 0/10000
        self.timeout = 4
        self.thread = None
        self.thread_calibrate = None
        self.status_calibrate = 0
    
    def voltage2stroke(self, pq12_index, voltage):
        stroke = (voltage - self.voltage_min[pq12_index]) / self.voltage_diff[pq12_index]
        stroke = round(stroke, 5)
        return stroke
    
    def stroke2voltage(self, pq12_index, stroke):
        voltage = stroke * self.voltage_diff[pq12_index] + self.voltage_min[pq12_index]
        voltage = round(voltage, 5)
        return voltage
    
    def start_pq12(self):
        if self.thread is None:
            # print(f'pq12_driver,start_pq12: no exisitng thread, start new thread')
            self.status = 1
            self.thread = threading.Thread(target=self.worker,)
            self.thread.start()

        else:
            # print(f'pq12_driver,start_pq12: terminating old thread')
            self.stop_pq12()
            self.thread.join()
            self.thread = None
            
            # print(f'pq12_driver,start_pq12: terminated old thread, start new thread')
            self.status = 1
            self.thread = threading.Thread(target=self.worker,)
            self.thread.start()

    def stop_pq12(self, ):
        self.status = 0
        # make pq12 go into idle
        for pq12_index in range(12):
            self.mcp_output(pq12_index, 0)
    
    def worker(self):
        # print stroke_target to console
        for pq12_index in range(12):
                if self.stroke_target[pq12_index] >= 0: 
                    print(f'pq12_driver,worker: worker{pq12_index} stroke_target:{self.stroke_target[pq12_index]}')
        t0 = time.time()
        # actuation loop
        while self.status == 1:
            # timeout exit condition
            if time.time() - t0 > self.timeout:
                self.status = 0
                for i in range(12):
                    if self.stroke_target[i] > -1:
                        self.mcp_output(i, 0)
                        self.stroke_diff[i] = round(self.stroke_target[i] - self.stroke_current[i], 5)						
                self.stop_pq12    
                print(f'pq12_driver, worker: timeout, exit worker')
                print(f'pq12_driver, worker: stroke_target: {self.stroke_target}') 
                print(f'pq12_driver, worker: stroke_current: {self.stroke_current}')
                print(f'pq12_driver, worker: stroke_diff: {self.stroke_diff}')                
                break
                
            # loop activities 
            for pq12_index in range(12):
                if self.stroke_target[pq12_index] > 0: 
                    # print(f'pq12_driver, worker:{pq12_index} t:{round((time.time() - t0)*1000, 3)}')
                    
                    self.voltage_current[pq12_index] = self.read_data(pq12_index)
                    if self.voltage_current[pq12_index] > 0:
                        self.stroke_current[pq12_index] = self.voltage2stroke(pq12_index, self.voltage_current[pq12_index])
                    else: 
                        self.stroke_current[pq12_index] = -1
                        # print(f'pq12_driver, worker: worker{pq12_index} voltage = -1')
                        
                    if self.stroke_current[pq12_index] == -1:
                        self.mcp_output(pq12_index, 0)      # idle 
                        # print(f'pq12_driver, worker: worker{pq12_index} adc_error, target stroke: {self.stroke_target[pq12_index]}') 
                    elif self.stroke_current[pq12_index] - self.stroke_target[pq12_index] < -1 * self.stroke_tolerance: 
                        self.mcp_output(pq12_index, 1)      # extrude
                    elif self.stroke_current[pq12_index] - self.stroke_target[pq12_index] > 1 * self.stroke_tolerance:
                        self.mcp_output(pq12_index, -1)      # retract
                    else:
                        self.mcp_output(pq12_index, 0)
                        print(f'pq12_driver, worker:{pq12_index} done, current stroke:{self.stroke_current[pq12_index]}, vol:{self.voltage_current[pq12_index]}') 
                        self.stroke_target[pq12_index] = -1
                
                # check whether all reach target stroke
                result = all(x == -1 for x in self.stroke_target)
                if result == True:
                    print(f'pq12_driver, worker: all reached target stroke, exit worker') 
                    self.status = 0
                    break;
                else:
                    # print(f'pq12_driver: pq12 worker, result=false, stroke_target {self.stroke_target}') 
                    time.sleep(self.interval)
        self.stop_pq12
                
    def mcp_output(self, pq12_index, value):
        if value == 1:          # extrude
            pin_A_value = 0
            pin_B_value = 1 
        elif value == -1:       # retract
            pin_A_value = 1
            pin_B_value = 0             
        elif value == 0:        # idle 
            pin_A_value = 0
            pin_B_value = 0    
        
        # if pq12_index < 4:
        #     self.mcp1.output(self.mcp1_pinA[pq12_index], pin_A_value)
        #     self.mcp1.output(self.mcp1_pinB[pq12_index], pin_B_value)
        # elif pq12_index < 8:
        #     self.mcp2.output(self.mcp2_pinA[pq12_index-4], pin_A_value)
        #     self.mcp2.output(self.mcp2_pinB[pq12_index-4], pin_B_value)   
        # else: 
        #     self.mcp3.output(self.mcp3_pinA[pq12_index-8], pin_A_value)
        #     self.mcp3.output(self.mcp3_pinB[pq12_index-8], pin_B_value)

        match pq12_index:
            case 0:
                self.mcp3.output(0, pin_A_value)
                self.mcp3.output(1, pin_B_value)
            case 1:
                self.mcp2.output(4, pin_A_value)
                self.mcp2.output(5, pin_B_value)
            case 2:
                self.mcp3.output(2, pin_A_value)
                self.mcp3.output(3, pin_B_value)
            case 3:
                self.mcp2.output(6, pin_A_value)
                self.mcp2.output(7, pin_B_value)  
            case 4:
                self.mcp3.output(4, pin_A_value)
                self.mcp3.output(5, pin_B_value)
            case 5:
                self.mcp2.output(2, pin_A_value)
                self.mcp2.output(3, pin_B_value)
            case 6:
                self.mcp3.output(6, pin_A_value)
                self.mcp3.output(7, pin_B_value)
            case 7:
                self.mcp2.output(0, pin_A_value)
                self.mcp2.output(1, pin_B_value)
            case 8:
                self.mcp1.output(0, pin_A_value)
                self.mcp1.output(1, pin_B_value)
            case 9:
                self.mcp1.output(5, pin_A_value)
                self.mcp1.output(6, pin_B_value)
            case 10:
                self.mcp1.output(2, pin_A_value)
                self.mcp1.output(3, pin_B_value)
            case 11:
                self.mcp1.output(7, pin_A_value)
                self.mcp1.output(8, pin_B_value)
        
    def read_data(self, pq12_index):
        if self.adc_channel_index[pq12_index] < 4:
            return round(self.adc1.read_data(self.adc_channel_index[pq12_index]),6)
        elif self.adc_channel_index[pq12_index] < 8:
            return round(self.adc2.read_data(self.adc_channel_index[pq12_index] - 4),6)
        elif self.adc_channel_index[pq12_index] < 12:
            return round(self.adc3.read_data(self.adc_channel_index[pq12_index] - 8),6)        
        else:
            return -1

    def start_calibrate(self):
        if self.thread_calibrate is None:
            print(f'pq12_driver, start_calibrate: no exisitng thread, start new thread')
            self.status_calibrate = 1
            self.thread_calibrate = threading.Thread(target=self.worker_calibrate,)
            self.thread_calibrate.start()

        else:
            print(f'pq12_driver, start_calibrate: terminating old thread')
            self.stop_calibrate()
            self.thread_calibrate.join()
            self.thread_calibrate = None
            
            print(f'pq12_driver, start_calibrate: terminated old thread, restart new thread')
            self.status_calibrate = 1
            self.thread_calibrate = threading.Thread(target=self.worker_calibrate,)
            self.thread_calibrate.start()

    def stop_calibrate(self):
        self.status_calibrate = 0
        # make pq12 go into idle
        for pq12_index in range(12):
            self.mcp_output(pq12_index, 0)
            
    def worker_calibrate(self):
        print(f'pq12_driver, worker_calibrate: extrude pq12 0 - 11')
        print(f'pq12_driver, worker_calibrate: retract pq12 0 - 11')
        print(f'pq12_driver, worker_calibrate: before calibration voltage_min: {self.voltage_min}')
        for pq12_index in range(0, 12): 
            self.mcp_output(pq12_index, -1)
        time.sleep(7)
        
        for pq12_index in range(0, 12): 
            self.mcp_output(pq12_index, 0)
            self.voltage_min[pq12_index] = self.read_data(pq12_index)
        print(f'pq12_driver, worker_calibrate: voltage_min: {self.voltage_min}')
        
        print(f'pq12_driver, worker_calibrate: before calibration voltage_max: {self.voltage_max}')
        for pq12_index in range(0, 12): 
            self.mcp_output(pq12_index, 1)
        time.sleep(7)
        
        for pq12_index in range(0, 12): 
            self.mcp_output(pq12_index, 0)
            self.voltage_max[pq12_index] = self.read_data(pq12_index)
        print(f'pq12_driver, worker_calibrate: voltage_max: {self.voltage_max}')
        
        
        for pq12_index in range(0, 12): 
            self.mcp_output(pq12_index, -1)
        time.sleep(7)
        
        for pq12_index in range(0, 12): 
            self.mcp_output(pq12_index, 0)
        
        '''    
        print(f'pq12_driver: calibrate, extrude pq12 6 - 11')
        for pq12_index in range(6, 12): 
            self.mcp_output(pq12_index, 1)
        time.sleep(1)
        
        for pq12_index in range(6, 12): 
            self.mcp_output(pq12_index, 0)
            self.voltage_max[pq12_index] = self.read_data(pq12_index)
        
        print(f'pq12_driver: calibrate, retract pq12 6 - 11')
        for pq12_index in range(6, 12): 
            self.mcp_output(pq12_index, -1)
        time.sleep(1)
        
        for pq12_index in range(6, 12): 
            self.mcp_output(pq12_index, 0)
            self.voltage_min[pq12_index] = self.read_data(pq12_index)
        '''
        
        for i in range(12):
            self.voltage_diff[i] = self.voltage_max[i] - self.voltage_min[i]
            self.voltage_diff[i] = round(self.voltage_diff[i], 3)
        
        print(f'pq12_driver, worker_calibrate: voltage_diff: {self.voltage_diff}')
    
    def set_stroke(self, stroke_list):
        for pq12_index in range(12):
            self.stroke_target[pq12_index] = round(stroke_list[pq12_index],3)
    
    def move(self, pq12_index, stroke):
        self.stroke_target[pq12_index] = round(stroke,3)

    def print_cycle_time(self):
        self.cycle_time_signal.emit(self.cycle_time, f'pq12')
                            
# driver test code
if __name__ == "__main__":
        mcp_address1 = 0x21
        mcp_address2 = 0x27
        mcp_address3 = 0x24
        
        mcp1 = MCP('MCP23008', mcp_address1)    
        mcp2 = MCP('MCP23017', mcp_address2)
        mcp3 = MCP('MCP23008', mcp_address3)
           
        mcp1.set_mode(0, 'output')
        mcp1.set_mode(1, 'output')
        mcp1.set_mode(2, 'output')
        mcp1.set_mode(3, 'output')
        mcp1.set_mode(4, 'output')
        mcp1.set_mode(5, 'output')
        mcp1.set_mode(6, 'output')
        mcp1.set_mode(7, 'output')
         
        mcp2.set_mode(0, 'output')
        mcp2.set_mode(1, 'output')
        mcp2.set_mode(2, 'output')
        mcp2.set_mode(3, 'output')
        mcp2.set_mode(4, 'output')
        mcp2.set_mode(5, 'output')
        mcp2.set_mode(6, 'output')
        mcp2.set_mode(7, 'output')
        mcp2.set_mode(8, 'output')
        mcp2.set_mode(9, 'output')
        mcp2.set_mode(10, 'output')
        mcp2.set_mode(11, 'output')
        mcp2.set_mode(12, 'output')
        mcp2.set_mode(13, 'output')
        mcp2.set_mode(14, 'output')
        mcp2.set_mode(15, 'output')
        
        mcp3.set_mode(0, 'output')
        mcp3.set_mode(1, 'output')
        mcp3.set_mode(2, 'output')
        mcp3.set_mode(3, 'output')
        mcp3.set_mode(4, 'output')
        mcp3.set_mode(5, 'output')
        mcp3.set_mode(6, 'output')
        mcp3.set_mode(7, 'output')
            
        for i in range(8):
            mcp1.output(i, 0)
        for i in range(16):
            mcp2.output(i, 0)
        for i in range(8):
            mcp3.output(i, 0)
            
        ADC_address1 = 0x48
        ADC_address2 = 0x49
        ADC_address3 = 0x4A
        # ADC_address4 = 0x4B
    
        adc1 = ADC(1, ADC_address1)
        adc2 = ADC(2, ADC_address2)
        adc3 = ADC(3, ADC_address3)
        # adc4 = ADC(4, ADC_address4)
        
        pq12 = PQ12(mcp1, mcp2, adc1, adc2, adc3)
        pq12.adc_channel_index = [3, 1, 7, 5, \
                                11, 9, 2, 0, \
                                8, 10, 4, 6]
        
        print('main pq12 init done')
        
        
        for pq12_index in range(12):
            print(f'pq12 {pq12_index}, retract')
            pq12.mcp_output(pq12_index, -1)
            # print(pq12.read_data(pq12_index))
        time.sleep(1)
        
        
        print('all pq12 sleep')
        for pq12_index in range(12):
            pq12.mcp_output(pq12_index, 0)
        
        # for feedback testing
        '''
        for pq12_index in range(7, 12):
            pq12.mcp_output(pq12_index, 1)
            time.sleep(0.3)
            pq12.mcp_output(pq12_index, 0)
            print(f'1st pq12_{pq12_index}, voltage = {pq12.read_data(pq12_index)}')
            pq12.mcp_output(pq12_index, 1)
            time.sleep(0.3)
            pq12.mcp_output(pq12_index, 0)
            print(f'2nd pq12_{pq12_index}, voltage = {pq12.read_data(pq12_index)}')
            pq12.mcp_output(pq12_index, 1)
            time.sleep(0.3)
            pq12.mcp_output(pq12_index, 0)
            print(f'3rd pq12_{pq12_index}, voltage = {pq12.read_data(pq12_index)}')
            
            pq12.mcp_output(pq12_index, -1)
            time.sleep(2)
            pq12.mcp_output(pq12_index, 0)
    '''
        
            
        pq12.voltage_max = [5.017, 4.988, 4.999, 5.017, 4.983, 5.017, 4.994, 4.949, 5.013, 4.993, 5.017, 4.987]

        pq12.voltage_min = [0.301, 0.305, 0.275, 0.302, 0.282, 0.29, 0.219, 0.308, 0.426, 0.259, 0.309, 0.28]

        for i in range(12):
                pq12.voltage_diff[i] = pq12.voltage_max[i] - pq12.voltage_min[i]
        
        # pq12.calibrate()
        
        # pinch stroke = [0.34, 0.32, 0.36, 0.37, \
        #                  0.37, 0.36, 0.54, 0.46 \
        #                  0.00, 0.43, 0.42, 0.43
        pq12.stroke_target = [0.01, 0.01, 0.01, 0.01, \
                                0.01, 0.01, 0.01, 0.01, \
                                0.01, 0.01, 0.01, 0.01]
        pq12.start_pq12()
        
        '''s
        for pq12_index in range(12):
                pq12.stroke_target[pq12_index] = pq12_index*0.05 + 0.3
                
        pq12.start_pq12()
        '''
        '''
        for pq12_index in range(12):
            for repeat in range(2):
                print(f'pq12 {pq12_index}, output 1')
                pq12.mcp_output(pq12_index, 1)
                time.sleep(1)
                
                # pq12.mcp_output(pq12_index, 0)
                # time.sleep(3)
                
                print(f'pq12 {pq12_index}, output 0')
                pq12.mcp_output(pq12_index, -1)
                time.sleep(1)
                
                pq12.mcp_output(pq12_index, 0)
                # time.sleep(3)
        '''
        
                
        # [pq12_index, adc_index]
        # pq12_index: 0 - 11
        # adc_index: 0 - 3 (adc1); 4 - 7 (adc2); 8 - 11 (adc3) 
        # 0, 3
        # 1, 1
        # 2, 7
        # 3, 5
        # 4, 11
        # 5, 9
        # 6, 2
        # 7, 0
        # 8, 6
        # 9, 4
        # 10, 10
        # 11, 8
        
        
        '''
        for i in range(5):
            pq12.move(i, 0.2 + i * 0.2)
        
        pq12.start_pq12()        
        '''
        
        
        # for i in range(4,12):
            # print(f'pq{i} extrude')
            # pq12.mcp_output(i, 1)
            # time.sleep(4)
            # print(f'pq{i} retract')
            # pq12.mcp_oupttut(i, -1)
            # time.sleep(4)
            # print(f'pq{i} idle')
            # pq12.mcp_output(i, 0)
        
