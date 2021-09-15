#!/usr/bin/env python3
import serial
import glob
import time
import sys
from enum import Enum

class dogUARTMaster():

    nominalInput = 512

    bodyRoll = 0
    bodyPitch = 0
    bodyYaw = 0
    bodyXoff = 0
    bodyYoff = 0
    bodyZoff = 0

    # Linear and angular gait velocities
    bodyWalkX = 0
    bodyWalkY = 0
    bodyWalkRotate = 0

    # Inputs for compatibility with single joystick
    yInput = nominalInput
    xInput = nominalInput

    # Instantiate empty serial object
    ser = serial.Serial()

    class controlMode(Enum):
        H_V = 0
        FB_Y = 1
        P_R = 2
        TRANS_ONE_LEG = 3 # Unused by teensy
        TRANS_TROT = 4
        ROTATE_ONE_LEG = 5 # Unused by teensy
        ROTATE = 6
    
    CM = controlMode.H_V

    def __init__(self, debugging=False, baudrate=115200):
        try:
            port = self.find_ports()[0]
            if debugging:
                print("using port {}".format(port))
            self.ser = serial.Serial(port, baudrate, timeout=1)
            time.sleep(0.1)
            self.ser.flush()
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
    
    def createSingleJoystickCommandStr(self):
        # Joystick command string consists of four digits for joystick Y, four digits for
        # joystick X, and one digit for the command mode: [123412341]
        return str(self.yInput).zfill(4) + str(self.xInput).zfill(4) + str(self.CM.value)

    def createCommandStr(self):
        # Full body command string consists of four digits for each orientation, four digits
        # for x and y velocities, and four digits for rotational velocity.
        return str(self.bodyRoll).zfill(4) + str(self.bodyPitch).zfill(4) + str(self.bodyYaw).zfill(4) \
            + str(self.bodyWalkX).zfill(4) + str(self.bodyWalkY).zfill(4) + str(self.bodyWalkRotate).zfill(4)

    def setControlModeJS(self, modeName):
        try:
            self.CM = self.controlMode[modeName]
            self.ser.write(self.createSingleJoystickCommandStr())
        except:
            print("Control mode not in list. Try one of 'H_V', 'FB_Y', 'P_R', 'TRANS_TROT', or 'ROTATE'")
    
    def setXInputJS(self, xIn):
        self.xInput = xIn
        self.ser.write(self.createSingleJoystickCommandStr())
    
    def setYInputJS(self, yIn):
        self.yInput = yIn
        self.ser.write(self.createSingleJoystickCommandStr())
    
    def setOnlyXInputJS(self, xIn):
        self.yInput = self.nominalInput
        self.xInput = xIn
        self.ser.write(self.createSingleJoystickCommandStr())
        
    def setOnlyYInputJS(self, yIn):
        self.yInput = yIn
        self.xInput = self.nominalInput
        self.ser.write(self.createSingleJoystickCommandStr())
    
    def setBothInputsJS(self, yIn, xIn):
        self.yInput = yIn
        self.xInput = xIn
        self.ser.write(self.createSingleJoystickCommandStr())
    
    def setAllJS(self, yIn, xIn, modeName):
        try:
            self.CM = self.controlMode[modeName]
            self.xInput = xIn
            self.yInput = yIn
            self.ser.write(self.createSingleJoystickCommandStr())
        except:
            print("Control mode not in list. Try one of 'H_V', 'FB_Y', 'P_R', 'TRANS_TROT', or 'ROTATE'")

    def setJoystickNominal(self):
        self.yInput = self.nominalInput
        self.xInput = self.nominalInput
        self.ser.write(self.createSingleJoystickCommandStr())

    def setRoll(self):
        # self.ser.write(self.)
        pass

    def setPitch(self):
        pass
    
    def setYaw(self):
        pass
    
    def rawInput(self, message):
        self.ser.write(message.encode('utf-8'))


    def printTeensyResponse(self):
        print("Response from Teensy: ")
        while self.ser.in_waiting > 0:
            line = self.ser.readline().decode('utf-8').rstrip()
            print(line)