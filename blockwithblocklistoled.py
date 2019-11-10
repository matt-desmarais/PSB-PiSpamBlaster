import serial
import time
from squid import *
import os.path
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
RST = None
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0
# Load default font.
font = ImageFont.load_default()

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
number = ""
name = ""
numberList = []
nameList = []
status = "waiting for call"
blockedLast = False

def drawScreen():
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    disp.clear()
    draw.text((x, top),       "Pi Spam Blaster",  font=font, fill=255)
    draw.text((x, top+8),     status, font=font, fill=255)
    draw.text((x, top+16),    "Name: "+str(name.decode('utf-8')),  font=font, fill=255)
    draw.text((x, top+25),    "Number: "+str(number.decode('utf-8')),  font=font, fill=255)
    #disp.clear()
    disp.image(image)
    disp.display()

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
    global status
    rgb.set_color(BLUE)
    if(number != None):
        with open("/home/pi/blockedNumbers.txt", "a") as numbersOutput:
            numbersOutput.write(number+"\n")
        status = "Last Caller Blocked!"
        drawScreen()
        loadBlocklist()
        time.sleep(1)
        rgb.set_color(OFF)

#setup callback for button func
GPIO.add_event_detect(button, GPIO.FALLING, callback=button_block, bouncetime=1000)

while True:
    try:
        disp.image(image)
        drawScreen()
        #get serial input
        line = ser.readline()
        #write modem output to file
        with open("/home/pi/modemOuput.txt", "a") as modemOutput:
            if(len(str(line)) != 1):
                modemOutput.write(str(line))
                print(line)
        #if phone rings turn led green
        if("RING" in str(line)):
            status = "last incoming call"
            #turn led green
            #rgb.set_color(GREEN)
        #store last number (to be blocked by button press)
        if("NMBR = " in str(line)):
            number  = str(line)[7:].rstrip('\r\n')
            disp.clear()
            print(number)
        if("NAME = " in str(line)):
            name  = str(line)[7:].rstrip('\r\n')
            disp.clear()
            print(name)
        if(blockedLast):
            with open("/home/pi/blockedCalls.txt", "a") as blockedCalls:
                blockedCalls.write(str(number)+" - "+str(name)+"\n")
            blockedLast = False
        #check for spam call or blocked caller id, also blocks numbers/names in textfiles
        if("NAME = SPAM?" in str(line) or "NMBR = P" in str(line) or str(line)[7:].rstrip('\r\n') in numberList or str(line)[7:].rstrip('\r\n').lower() in nameList):
            blockedLast = True
            status = "LAST CALL BLOCKED!"
            drawScreen()
            #turn led red
            rgb.set_color(RED)
            #answer call
            ser.write('ATA'+'\r\n')
            time.sleep(12)
            #hangup
            ser.write('ATH0'+'\r\n')
            #flush serial
            #ser.flushInput()
            rgb.set_color(OFF)
    except KeyboardInterrupt:
        print("Keyboard Interrupt")
        break
