#!/usr/bin/env python
#
# rpio implementation and calc: 
#   https://cdn-learn.adafruit.com/downloads/pdf/adafruits-raspberry-pi-lesson-8-using-a-servo-motor.pdf
# how clock works:
#   http://raspberrypi.stackexchange.com/questions/4906/control-hardware-pwm-frequency
#
#
import wiringpi
from time import sleep

# Define GPIO pins
wiringpi.wiringPiSetupGpio()
PIN_PWM = 18  # pin 12
PIN_DOOR = 7  # pin 26

# Set up pins
wiringpi.pinMode(PIN_PWM, 2) 
wiringpi.pinMode(PIN_DOOR, 0)

# Setup PWM clock
wiringpi.pwmSetMode(wiringpi.PWM_MODE_MS)
wiringpi.pwmSetClock(192)
wiringpi.pwmSetRange(2000)

def servoControl(open=False):
    if open:
        print 'opening...'
        wiringpi.pwmWrite(PIN_PWM,235)
    else:
        wiringpi.pwmWrite(PIN_PWM,53)
        print 'closing...'
    sleep(3)

timeout = 120
try:
    servoControl(open=True)	
    # Wait until door opens or timeout
    while wiringpi.digitalRead(PIN_DOOR) == 0 and timeout > 0:
        timeout -= 1
        sleep(1)
    sleep(2)

except KeyboardInterrupt:  # Catch this to close the door if Ctrl+C
    pass

servoControl(open=False)
