#!/usr/bin/env python3
import serial
import glob
import time
import sys
from enum import Enum

class dogUARTMaster():
    yInput = 0
    xInput = 0

    class controlMode(Enum):
        H_V = 0
        FB_Y = 1
        P_R = 2
        TRANS_ONE_LEG = 3 # Unused by teensy
        TRANS_TROT = 4
        ROTATE_ONE_LEG = 5 # Unused by teensy
        ROTATE = 6
    
    CM = controlMode.H_V

    def __init__(self, debugging=True, baudrate=115200):
        try:
            port = self.find_ports()[0]
            if debugging:
                print("using port {}".format(port))
            self.ser = serial.Serial(port, baudrate, timeout=1)
            time.sleep(0.1)
            self.ser.flush()
            # while True:
            #     if self.ser.in_waiting > 0:
            #         line = self.ser.readline().decode('utf-8').rstrip()
            #         print(line)
            #         ser.flush()
            #     inp = raw_input(">>>> ")
            #     self.ser.write(inp.encode('utf-8'))
        except:
            print("Error finding port. Make sure Teensy is powered on and USB is connected to Pi.")

    def find_ports(self):
        ports = glob.glob('/dev/ttyACM[0-9]*')

        res = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                res.append(port)
            except:
                pass
        return res
    
    def createCommandStr(self):
        return str(self.yInput).zfill(4) + str(self.xInput).zfill(4) + str(self.CM.value)

    def setControlMode(self, modeName):
        try:
            CM = self.controlMode['modeName']
            self.ser.write(self.createCommandStr())
        except:
            print("Control mode not in list. Try one of 'H_V', 'FB_Y', 'P_R', 'TRANS_TROT', or 'ROTATE'")
    
    def setXInput(self, xIn):
        self.xInput = xIn
        self.ser.write(self.createCommandStr())
    
    def setYInput(self, yIn):
        self.yInput = yIn
        self.ser.write(self.createCommandStr())
    
    def setOnlyXInput(self, xIn):
        self.yInput = 0
        self.xInput = xIn
        self.ser.write(self.createCommandStr())
        
    def setOnlyYInput(self, yIn):
        self.yInput = yIn
        self.xInput = 0
        self.ser.write(self.createCommandStr())
    
    def setBothInputs(self, yIn, xIn):
        self.yInput = yIn
        self.xInput = xIn
        self.ser.write(self.createCommandStr())
    
    def setAll(self, yIn, xIn, modeName):
        try:
            self.CM = self.controlMode['modeName']
            self.xInput = xIn
            self.yInput = yIn
            self.ser.write(self.createCommandStr())
        except:
            print("Control mode not in list. Try one of 'H_V', 'FB_Y', 'P_R', 'TRANS_TROT', or 'ROTATE'")
    