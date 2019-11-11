import serial
import time
from squid import *
import os.path
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
#set button pin number
button = 26
#setup button
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#setup serial
ser = serial.Serial('/dev/ttyACM0')
#setup led
rgb = Squid(16, 20, 21)
#flush serial
ser.flushInput()
#print serial interface
print(ser.name)
#test modem
ser.write('AT'+'\r\n')
#zero out modem settings
ser.write('ATZ'+'\r\n')
#turn caller id on
ser.write('AT+VCID=1'+'\r\n')
#number block list file
numbers = "/home/pi/blockedNumbers.txt"
#name block list file
names = "/home/pi/blockedNames.txt"
#setup variables
number = None
numberList = []
nameList = []
blockedLast = False

#func to load name/number blocklists
def loadBlocklists():
    global numberList
    global nameList
    #if number block list exists load it
    if(os.path.isfile(numbers)):
        numberList = [line.rstrip(' \r\n') for line in open(numbers)]
        numberList = filter(None, numberList)
        print("Blocked Numbers: "+str(numberList))
    #if name block list exist load it
    if(os.path.isfile(names)):
        nameList = [line.rstrip(' \r\n').lower() for line in open(names)]
        nameList = filter(None, nameList)
        print("Blocked names: "+str(nameList))

#func to load blocklist numbers file
def loadBlocklist():
    global numberList
    #if number block list exists load it
    if(os.path.isfile(numbers)):
        numberList = [line.rstrip(' \r\n') for line in open(numbers)]
        numberList = filter(None, numberList)

loadBlocklists()

#func button callback to add last number to blocklist
def button_block(channel):
    rgb.set_color(BLUE)
    if(number != None):
        with open(numbers, "a") as numbersOutput:
            numbersOutput.write(number)
        loadBlocklist()
        time.sleep(1)
        rgb.set_color(OFF)

#setup callback for button func
GPIO.add_event_detect(button, GPIO.FALLING, callback=button_block, bouncetime=1000)

while True:
    try:
        #get serial input
        line = ser.readline()
        #write modem output to file
        with open("/home/pi/modemOuput.txt", "a") as modemOutput:
            if(len(str(line)) != 1):
                modemOutput.write(str(line))
                print(line)
        #get date and time
        if("DATE = " in str(line)):
            date  = str(line)[7:].rstrip('\r\n')
        if("TIME = " in str(line)):
            timeofcall  = str(line)[7:].rstrip('\r\n')
        #store last number (to be blocked by button press)
        if("NMBR = " in str(line)):
            number  = str(line)[7:].rstrip('\r\n')
        if("NAME = " in str(line)):
            name  = str(line)[7:].rstrip('\r\n')
        if(blockedLast):
            with open("/home/pi/blockedCalls.txt", "a") as blockedCalls:
                blockedCalls.write(str(date)+" - "+str(timeofcall)+" - "+str(number)+" - "+str(name)+"\n")
            blockedLast = False
        #check for spam call or blocked caller id, also blocks numbers/names in textfiles
        if("NAME = SPAM?" in str(line) or "NMBR = P" in str(line) or str(line)[7:].rstrip('\r\n') in numberList or str(line)[7:].rstrip('\r\n').lower() in nameList):
            blockedLast = True
            #turn led red
            rgb.set_color(RED)
            #answer call
            ser.write('ATA'+'\r\n')
            time.sleep(12)
            #hangup
            ser.write('ATH0'+'\r\n')
            #flush serial
            #ser.flushInput()
    except KeyboardInterrupt:
        print("Keyboard Interrupt")
        break
