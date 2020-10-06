## Setup LCD Scripts
These are just misc scripts I used; use the installer associated with this repo: https://github.com/the-raspberry-pi-guy/lcd


```bash
sudo apt-get update && sudo apt-get install -y i2c-tools
```


```bash
git clone https://github.com/the-raspberry-pi-guy/lcd
cd lcd
sudo bash install.sh

```

```bash
sudo raspi-config
> Interfacing Options > I2C > Enable
sudo reboot

```

```bash
sudo i2cdetect -y 1
```

Install low level deps
```bash
sudo apt-get update && sudo apt-get -y install python-smbus
revision=`python -c "import RPi.GPIO as GPIO; print GPIO.RPI_REVISION"`
if [ $revision = "1" ]; then
    cp installConfigs/i2c_lib_0.py ./i2c_lib.py
else
    cp installConfigs/i2c_lib_1.py ./i2c_lib.py
fi;
cp installConfigs/modules /etc/
cp installConfigs/raspi-blacklist.conf /etc/modprobe.d/
printf "dtparam=i2c_arm=1\n" >> /boot/config.txt
read -n1 -s
sudo reboot
```
