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
PIN_RINGER = 10  # pin 19
PIN_EXTERNAL_DOOR = 24  # pin 18 

# Set up pins
wiringpi.pinMode(PIN_PWM, wiringpi.PWM_OUTPUT) 
wiringpi.pinMode(PIN_EXTERNAL_DOOR, wiringpi.OUTPUT)
wiringpi.pinMode(PIN_DOOR, wiringpi.INPUT)
wiringpi.pinMode(PIN_RINGER, wiringpi.INPUT)
wiringpi.pullUpDnControl(PIN_RINGER, wiringpi.PUD_DOWN)

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

# Initialize
timeout = 120
wiringpi.digitalWrite(PIN_EXTERNAL_DOOR,wiringpi.LOW)

try:
    
    print "Waiting for someone to ring..."
    while wiringpi.digitalRead(PIN_RINGER) == 0:
        sleep(0.4)

    print " * Someone there. Opening external door..."
    wiringpi.digitalWrite(PIN_EXTERNAL_DOOR, wiringpi.HIGH)
    sleep (5)
    wiringpi.digitalWrite(PIN_EXTERNAL_DOOR, wiringpi.LOW)

    print " * Closing external door. Opening your home..."
    servoControl(open=True)	
    # Wait until door opens or timeout
    while wiringpi.digitalRead(PIN_DOOR) == 0 and timeout > 0:
        timeout -= 1
        sleep(1)
    if timeout > 0:
        print " * Someone just get in"
    else:
        print " * Nobody there and timeout exceeded"
    sleep(2)

except KeyboardInterrupt:  # Catch this to close the door if Ctrl+C
    pass

print " * Closing everything"
wiringpi.digitalWrite(PIN_EXTERNAL_DOOR, wiringpi.LOW)
servoControl(open=False)
