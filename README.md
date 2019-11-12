# PSB-PiSpamBlaster
Telephone spam silencer based on caller id. My service provider [Verizon](https://www.verizon.com/about/news/block-spam-robocalls-with-verizon-new-tool) prefixes the caller id of spam calls with SPAM?.
I also block calls with blocked called IDs. The calls are answered by the modem which makes loud tones for 12 seconds.
There are 2 blocklists files that you can put numbers/names in to be blocked. The numbers file can be added to by pressing
the the button attached to pin 26 to block the last incoming phone number, the name will not be blocked. 
The RGB LED is wired to [GND][16][20][21] - [GND][R][G][B]. the button is attached to GND and pin 26. The oled fits on at the top of the header.<br/>
![PSB Device](https://github.com/matt-desmarais/PSB-PiSpamBlaster/raw/master/IMG_20191109_205748.jpg)

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
