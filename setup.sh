#!/bin/bash

# Update system
apt update
apt upgrade -y
apt-get install build-essential cmake unzip pkg-config libjpeg-dev libpng-dev libtiff-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libgtk-3-dev libatlas-base-dev gfortran python3-dev python3-scipy -y
apt clean

# Create swap file
fallocate -l 2G /swapfile
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile

# Mount sd card
mkdir /mnt/sd
mount /dev/mmcblk1p1 /mnt/sd

# Build opencv
cd /mnt/sd
wget -O opencv.zip https://github.com/opencv/opencv/archive/4.1.0.zip
unzip opencv.zip
cd /mnt/sd/opencv-4.1.0
mkdir /mnt/sd/opencv-4.1.0/build && cd /mnt/sd/opencv-4.1.0/build
cmake -D CMAKE_BUILD_TYPE=RELEASE \
 -D CMAKE_INSTALL_PREFIX=/usr/local \
 -D OPENCV_ENABLE_NONFREE=ON \
 -D PYTHON3_EXECUTABLE=$(which python3) \
 -D PYTHON3_PACKAGES_PATH=$(python3 -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())") \
 -D ENABLE_NEON=ON \
 -D WITH_V4L=ON ..
make -j4
make install

# Install pip packages
pip3 install --no-cache-dir -r /home/mendel/Project3/MachineLearning/requirements.txt
pip3 install --no-cache-dir -r /home/mendel/Project3/Backend/requirements.txt

# Create certificate
cd /home/mendel
openssl req -x509 -nodes -newkey rsa:2048 -keyout rsa_private.pem -out rsa_cert.pem -subj "/CN=unused"

# Set hostname
if [ "$1" != "" ]; then
    echo "$1" > /etc/hostname
    hostname "$1"
fi

# Set environment variables
export GOOGLE_APPLICATION_CREDENTIALS=/home/mendel/Project3-ML6-420c2216d454.json
export DEVICE_ID=$HOSTNAME
export RSA_CERT=/home/mendel/rsa_cert.pem

# Run create device
python3 /home/mendel/Project3/Backend/create_device.py

# Setup service
cp /home/mendel/Project3/project3.service /etc/systemd/system/
systemctl enable project3

# Reboot
reboot
