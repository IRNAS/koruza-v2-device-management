# koruza-v2-device-management

https://www.instructables.com/Control-Bluetooth-LE-Devices-From-A-Raspberry-Pi/

1. Remove existing bluez installation with `sudo apt-get --purge remove bluez`
2. Get latest bluez package `cd ~; wget https://mirrors.edge.kernel.org/pub/linux/bluetooth/bluez-5.9.tar.xz`
3. Unpack with `tar xvf bluez-5.9.tar.xz`
4. Install required packages with 
`sudo apt-get install libusb-dev libdbus-1-dev libglib2.0-dev libudev-dev libical-dev libreadline-dev`
5. To compile and install bluez first move into the directory with `cd bluez-5.9`
6. Execute
```
export LDFLAGS=-lrt
./configure --prefix=/usr --sysconfdir=/etc --localstatedir=/var --enable-library -disable-systemd 
make
sudo make install
sudo cp attrib/gatttool /usr/bin/
```
Raspberry Pi ble help: https://www.argenox.com/library/bluetooth-low-energy/using-raspberry-pi-ble/
