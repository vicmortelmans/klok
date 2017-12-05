#!/bin/sh
setxkbmap us
echo 'Europe/Brussels' | sudo tee /etc/timezone
sudo dpkg-reconfigure -f noninteractive tzdata

