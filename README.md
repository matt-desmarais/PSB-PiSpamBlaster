# PSB-PiSpamBlaster
Telephone spam silencer based on caller id

Parts:<br/>
    Pi Zero W<br/>
    USB Dialup Modem<br/>
    Micro SD Card<br/>
    Mini Micro USB OTG Adapter<br/>
    Squid prewired RGB LED<br/>
    GPIO Button<br/>
    optional:<br/>
        Adafruit Pi Oled<br/>

Operating System:<br/>
    Buster Lite<br/>

Software to install:<br/>
    sudo apt-get install python-pip git<br/>
    sudo pip install pyserial<br/>
    git clone https://github.com/simonmonk/squid.git<br/>
    cd squid<br/>
    sudo python setup.py install<br/>

Clone code:<br/>
    git clone https://github.com/matt-desmarais/PSB-PiSpamBlaster.git<br/>

optional software for Oled<br/>
    sudo apt-get install python-pil python-smbus<br/>
    git clone https://github.com/adafruit/Adafruit_Python_SSD1306.git<br/>
    cd Adafruit_Python_SSD1306<br/>
    sudo python setup.py install<br/>
    
Add numbers to blocklist:<br/>
    /home/pi/blockedNumbers.txt<br/>

Add names to blocklist:<br/>
    /home/pi/blockedNames.txt<br/>

Autorun at boot<br/>
run crontab -e<br/>
add next line to end of file<br/>
@reboot sudo python /home/pi/PSB-PiSpamBlaster/blockwithblocklist.py<br/>
if usinging PiOled then use this next line instead<br/>
@reboot sudo python /home/pi/PSB-PiSpamBlaster/blockwithblocklistoled.py<br/>
