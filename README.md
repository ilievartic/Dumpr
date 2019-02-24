# ParkMe
### HackIllinois 2019
made by Ilie, Shang, Vassily, Prerak, and Sharang 

### What is ParkMe?
ParkMe is an automated parking-meter platform. A camera in each parking spot recognizes a car's license plate, and automatically charges the associated account based on the amount of time the car stays in the parking spot.

The "smart parking meter" runs on a Raspberry Pi, and can transmit license plate/timestamp data to a centralized server via WiFi. These parking meters are also portable, as the raspberry pi can be connected to an LTE endpoint. In this way, users can buy a fairly cheap meter and convert part of their own property into a paid parking spot. (This can be used, for example, on a football gameday where parking near a stadium may be scarce.) This repository contains a proof-of-concept demo of the parking meter communicating with the server over LTE, using the Particle Boron IoT platform.

### Building and Running

#### Pi Backend
The backend is intended to run on a low power embedded device such as a Raspberry Pi.
The device has a V4L2 camera device attached and a serial link with the LTE device for data transmission. There is also an optional Wifi transmission backend in the event that LTE is not available.
Prerequisites:
+ OpenAlpr (Plate Recognition)
+ Python2
+ OpenCV
+ pySerial
+ fbi (framebuffer imageviewer) (optional)

Simply running the python script with `./platescan.py` will begin plate scanning and transmit over serial. Optinally setting the flag `sendWifi` to true will disable the LTE over serial connection and will send data over wifi.
Optionally, view frames on an attached monitor the script `./viewer.sh` can be used.
###Particle Boron and Xenon Setup

Particle is a upcoming startup company with microcontroller boards aiding IoT. We used the particle boron and the particle xenon boards supporting LTE and ethernet each respectively. We used a featherwing adapter board for the xenon. Installed cli on our laptops and setup, authenticated and identified serial numbers of the boards. We used a Google Project Fi LTE data card for the boron board in order to improve poratability and show the usage of this board in remote areas without wifi access. Connected both boards to the internet, waited for confirmation from the lights, wrote the code for the board and flashed it using particle cloud.

#### Web backend:
npm install, node server.js


### Contributing

If you would like to contribute to ParkMe, check out [our contribution guide](CONTRIBUTING.md).

### Licensing

ParkMe is open-source software, licensed under GNU's Lesser GPL. This means anyone can link ParkMe source code in their own projects. Any use or modification of this code must be open-source licensed.
