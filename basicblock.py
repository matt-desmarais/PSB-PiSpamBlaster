import serial
import time
ser = serial.Serial('/dev/ttyACM0')
ser.flushInput()
print(ser.name) 
#test modem
ser.write('AT'+'\r\n')
#zero out modem settings
ser.write('ATZ'+'\r\n')
#turn caller id on
ser.write('AT+VCID=1'+'\r\n')
#ignore wait for dial tone for dialing
ser.write('ATX1'+'\r\n')
#speed of tone dialing in ms
ser.write('ATS11=50'+'\r\n')

while True:
    try:
        #get serial input
        line = ser.readline()
        with open("modemOuput.txt", "a") as modemOutput:
            if(len(str(line)) != 1):
                modemOutput.write(str(line))
                print(line)
        print(line)
        #check for spam call or blocked caller id
        if("NAME = SPAM?" in str(line) or "NMBR = P" in str(line)):
            #answer modem
            ser.write('ATA'+'\r\n')
            time.sleep(12)
            #hangup
            ser.write('ATH0'+'\r\n')
    except KeyboardInterrupt:
        print("Keyboard Interrupt")
        break
