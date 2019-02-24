#!/bin/bash
sudo killall fbi
rm /tmp/plate.jpg.1 /tmp/plate.jpg.2 2>/dev/null
ln -s /tmp/plate.jpg /tmp/plate.jpg.1
ln -s /tmp/plate.jpg /tmp/plate.jpg.2
sudo fbi -d /dev/fb0 -T 1 -noverbose -cachemem 0 /tmp/plate.jpg /tmp/plate.jpg.1 /tmp/plate.jpg.2
