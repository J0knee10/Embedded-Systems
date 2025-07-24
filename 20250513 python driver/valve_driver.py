from typing import Type
from MCP_driver import MCP
import time
import threading
import pigpio
from PyQt5.QtCore import pyqtSignal

class Valve():
    
    def __init__(self, mcp: Type[MCP]):
        self.mcp = mcp
        self.status = [0, 0, 0, 0, 0, 0, 0, 0]
        # correspond mcp channel index to valve index
        # self.mcp_channel_index = [valve1, valve2, valve3.....]
        self.mcp_channel_index = [-1, -1, -1, -1, -1, -1, -1, -1]
        
    def actuate(self, level):
        for valve_index in range(8): 
            if level[valve_index] >=0: self.mcp.output(self.mcp_channel_index[valve_index], level[valve_index])
            self.status[valve_index] = level[valve_index]
        
    def all_on(self):
        for valve_index in range(8): 
            self.mcp.output(self.mcp_channel_index[valve_index], 1)
            self.status[valve_index] = 1
            
    def all_off(self):
        for valve_index in range(8): 
            self.mcp.output(self.mcp_channel_index[valve_index], 0)
            self.status[valve_index] = 0


# driver test code
if __name__ == "__main__":
    
    # PQ12 board
    # MCP23008 address [A0, A1, A2] = [High, Low, Low], 0x21
    # MCP23017 address [A0, A1, A2] = [High, High, High], 0x27
    
    # stepper driver board
    # MCP23008 address [A0, A1, A2] = [Low Low, High], 0x24

    address1 = 0x27
    address2 = 0x21
    address3 = 0x24
        
    # MCP1 = MCP('MCP23017', address1)
    # MCP2 = MCP('MCP23008', address2)
    MCP3 = MCP('MCP23008', address3)
    
    # output tests
    # print('start output test')
    # MCP1.set_mode(0, 'output')
    # MCP1.set_mode(1, 'output')
    # MCP1.set_mode(2, 'output')
    # MCP1.set_mode(3, 'output')
    # MCP1.set_mode(4, 'output')
    # MCP1.set_mode(5, 'output')
    # MCP1.set_mode(6, 'output')
    # MCP1.set_mode(7, 'output')
    # MCP1.set_mode(8, 'output')
    # MCP1.set_mode(9, 'output')
    # MCP1.set_mode(10, 'output')
    # MCP1.set_mode(11, 'output')
    # MCP1.set_mode(12, 'output')
    # MCP1.set_mode(13, 'output')
    # MCP1.set_mode(14, 'output')
    # MCP1.set_mode(15, 'output')
    
    
    # MCP2.set_mode(0, 'output')
    # MCP2.set_mode(1, 'output')
    # MCP2.set_mode(2, 'output')
    # MCP2.set_mode(3, 'output')
    # MCP2.set_mode(4, 'output')
    # MCP2.set_mode(5, 'output')
    # MCP2.set_mode(6, 'output')
    # MCP2.set_mode(7, 'output')
    
    MCP3.set_mode(0, 'output')
    MCP3.set_mode(1, 'output')
    MCP3.set_mode(2, 'output')
    MCP3.set_mode(3, 'output')
    MCP3.set_mode(4, 'output')
    MCP3.set_mode(5, 'output')
    MCP3.set_mode(6, 'output')
    MCP3.set_mode(7, 'output')
    
    MCP3.output(0, 0)
    MCP3.output(1, 0)
    MCP3.output(2, 0)
    MCP3.output(3, 0)
    MCP3.output(4, 0)
    MCP3.output(5, 0)
    MCP3.output(6, 0)
    MCP3.output(7, 0)
    print('MCP3 initialized')
    
    valve = Valve(MCP3)
    valve.mcp_channel_index = [0, 1, 2, 3, 4, 5, 6, 7]
    valve.all_on()
    time.sleep(2)
    valve.all_off()
    time.sleep(2)
    
