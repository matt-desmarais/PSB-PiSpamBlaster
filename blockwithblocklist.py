import serial
import time
from squid import *
import os.path
import RPi.GPIO as GPIO
button = 26
GPIO.setmode(GPIO.BCM)
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
ser = serial.Serial('/dev/ttyACM0')
rgb = Squid(16, 20, 21)
ser.flushInput()
print(ser.name)
#test modem
ser.write('AT'+'\r\n')
#zero out modem settings
ser.write('ATZ'+'\r\n')
#turn caller id on
ser.write('AT+VCID=1'+'\r\n')
number = None
numbers = "/home/pi/blockedNumbers.txt"
numberList = []

def loadBlocklists():
    if(os.path.isfile(numbers)):
        numberList = [line.rstrip('\n') for line in open(numbers)]

loadBlocklists()

def button_block(channel):
    rgb.set_color(BLUE)
    if(number != None):
        with open("blockedNumbers.txt", "a") as numbersOutput:
            numbersOutput.write(number)
        loadBlocklists()
        time.sleep(1)
        rgb.set_color(OFF)

GPIO.add_event_detect(button, GPIO.FALLING, callback=button_block, bouncetime=1000)

while True:
    try:
        rgb.set_color(OFF)
        #get serial input
        line = ser.readline()
        with open("modemOuput.txt", "a") as modemOutput:
            if(len(str(line)) != 1):
                modemOutput.write(str(line))
                print(line)
        if("RING" in str(line)):
            rgb.set_color(GREEN)
        if("NMBR = " in str(line)):
            number  = str(line)
        #check for spam call or blocked caller id, also blocks numbers/names in textfiles
        if("NAME = SPAM?" in str(line) or "NMBR = P" in str(line) or str(line)[7:].rstrip() in numberList or str(line)[7:].rstrip() in nameList):
            rgb.set_color(RED)
            #answer call
            ser.write('ATA'+'\r\n')
            time.sleep(12)
            #hangup
            ser.write('ATH0'+'\r\n')
            #flush serial
            ser.flushInput()
            #turn led off
            rgb.set_color(OFF)
    except KeyboardInterrupt:
        print("Keyboard Interrupt")
        break
