
from CamDeviceConfig import deviceconfig
from Actuators import LedIndicator
from Inputs import IoInputs


import RPi.GPIO as GPIO
import time

#Start...
#TODO: make use of configfile
GPIO.setmode(GPIO.BCM)
redButton = IoInputs.PushButton(GPIO, 15)
greenButton = IoInputs.PushButton(GPIO, 14)
switch = IoInputs.OnOnSwitch(GPIO, 21, 12)

redButton.initialize()
greenButton.initialize()
switch.initialize()

redLed =  LedIndicator.LedIndicator(GPIO, 24)
greenLed = LedIndicator.LedIndicator(GPIO, 23)
yellowLed = LedIndicator.LedIndicator(GPIO, 22)

print "Start testing...."
print "RedLed... On"
redLed.activate(True)
time.sleep(1)

print "GreenLed... On"
greenLed.activate(True)
time.sleep(1)

print "YellowLed... On"
yellowLed.activate(True)
time.sleep(1)

running = True
while(running):
    try:
        print "RedButtonState: " + str(redButton.update())
        print "GreenButtonState: " + str(greenButton.update())
        print "SwitchState" + str(switch.update())
        time.sleep(0.2)
    except:
        running= False

GPIO.cleanup()
print "Test is done..."






