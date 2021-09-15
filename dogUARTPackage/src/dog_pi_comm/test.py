import piMasterUART
import time

cont = piMasterUART.dogUARTMaster(debugging=True)
time.sleep(0.3)
print(".")
time.sleep(0.3)
print(".")
time.sleep(0.3)
print(".")
time.sleep(0.3)
print("starting")
time.sleep(0.3)

def runGamut(controlMode):
    print("setting control mode to {}".format(controlMode))
    cont.setControlModeJS(controlMode)
    time.sleep(1)

    print("set x and y to 512")
    cont.setXInputJS(512)
    cont.setYInputJS(512)
    time.sleep(2)

    print("set x to 700")
    cont.setXInputJS(700)
    time.sleep(2)

    print("set y to 700")
    cont.setYInputJS(700)
    time.sleep(2)

    print("set x to 300")
    cont.setXInputJS(300)
    time.sleep(2)

    print("set y to 300")
    cont.setYInputJS(300)
    time.sleep(2)

    print("set inputs nominal")
    cont.setJoystickNominal()
    time.sleep(2)

    print("set both inputs 700, 300")
    cont.setBothInputsJS(700, 300)
    time.sleep(2)

    print("set inputs nominal")
    cont.setJoystickNominal()
    time.sleep(2)

    print("done")

runGamut('H_V')
runGamut('FB_Y')
runGamut('P_R')
runGamut('TRANS_TROT')
runGamut('ROTATE')