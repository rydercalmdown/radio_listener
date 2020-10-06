#!/bin/bash

# Install lower level dependencies.
echo "Install lower level dependencies outlined in readme"

echo "Installing python"
cd /home/pi/radio_listener
virtualenv env
. env/bin/activate
pip install -r requirements.txt

echo "Fixing pyacrcloud for raspberry pi"
pip uninstall -y pyacrcloud
cd /home/pi
git clone https://github.com/acrcloud/acrcloud_sdk_python.git
cd /home/pi/acrcloud_sdk_python/raspberrypi/aarch32/python3 && python setup.py install
rm -rf /home/pi/acrcloud_sdk_python/
cd /home/pi/radio_listener

# echo "Installing LCD Driver"
# cd /home/pi
# git clone https://github.com/the-raspberry-pi-guy/lcd
# cd /home/pi/lcd/
# echo "run install.sh manually in /home/pi/lcd/"
# mv /home/pi/lcd/lcddriver.py /home/pi/radio_listener
# mv /home/pi/lcd/i2c_lib.py /home/pi/radio_listener
# rm -rf /home/pi/lcd/
