#!/usr/bin/env bash

export LANG='en_US.UTF-8'
export LC_ALL='en_US.UTF-8'
# Install pip3
version=$(python3 --version | cut -d '.' -f 2)
echo "Python version 3.${version}"
sudo apt-get install python3-pip
sudo pip3 install requests
sudo pip3 install Django
sudo pip3 install pathlib

