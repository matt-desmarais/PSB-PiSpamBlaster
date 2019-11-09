# PSB-PiSpamBlaster
Telephone spam silencer based on caller id

Parts:
    Pi Zero W
    USB Dialup Modem
    Micro SD Card
    Mini Micro USB OTG Adapter
    Squid prewired RGB LED
    GPIO Button
    optional:
        Adafruit Pi Oled

Operating System:
    Buster Lite

Software to install:
    sudo apt-get install python-pip git
    sudo pip install pyserial

Clone code:
    git clone https://github.com/matt-desmarais/PSB-PiSpamBlaster.git
    
Add numbers to blocklist:
    /home/pi/blockedNumbers.txt

Add names to blocklist:
    /home/pi/blockedNames.txt

Autorun at boot
run crontab -e
add next line to end of file
@reboot sudo python /home/pi/PSB-PiSpamBlaster/blockwithblocklist.py 
