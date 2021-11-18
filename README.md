# Jetson Nano - Initial Setup
The whole kit we are using is one offered by Sparkfun:
<a href="https://www.sparkfun.com/products/retired/16417" target="_blank">
    Sparkfun JetBot AI Kit v2.1 Powered by Jetson Nano
</a>

For the initial setup, you'll need the following items:
- Monitor
- HDMI cable
- Mouse
- Keyboard
- Ethernet cable for internet.

## JetPack 4.6
First, for our case, we are using the Jetson Nano Developer Kit, which has
4GB of memory, and we installed the JetPack 4.6 on a formatted SD card. Attention
to the type of your microSD card, because at least by the time we used, we
needed a very specific type of microSD card.

Also, when formatting the microSD card, prefer to convert it to
`EXT4` format, which can be done using the `Disks` program, found in many linux
distributions already installed, or the program of your choice.

Link to download the JetPack 4.6 SD card image:
<a href="https://developer.nvidia.com/jetson-nano-sd-card-image" target="_blank">
    JetPack 4.6
</a>

After downloading the image, you can follow the steps on the NVIDIA Developer
Getting Started guide to flash the image to a microSD card:
<a href="https://developer.nvidia.com/embedded/learn/get-started-jetson-nano-devkit#write" target="_blank">
    Getting Started with Jetson Nano Developer Kit
</a>

## Wifi Adapter - Edimax N150
The next steps can be found in the Sparkfun page:
<a href="https://learn.sparkfun.com/tutorials/adding-wifi-to-the-nvidia-jetson/all#driver-installation" target="_blank">
    Sparkfun - Driver Installation
</a>

Also some of the commands can be found directly in the Github repository of
the driver:
<a href="https://github.com/lwfinger/rtl8723bu" target="_blank">
    rtl8723bu Github Page
</a>

For the wifi adapter to work, we need to install its drivers. For that, inside
the Jetson, first clone this repository:

```
git clone https://github.com/lwfinger/rtl8723bu.git
cd rtl8723bu/
```

After that, for an automatic install, we need to install the DKMS package:

```
sudo apt update
sudo apt install dkms
```

Finally, paste the following commands in the terminal, inside the rtl8723bu folder:

```
source dkms.conf
sudo mkdir /usr/src/$PACKAGE_NAME-$PACKAGE_VERSION
sudo cp -r core hal include os_dep platform dkms.conf Makefile rtl8723b_fw.bin /usr/src/$PACKAGE_NAME-$PACKAGE_VERSION
sudo dkms add $PACKAGE_NAME/$PACKAGE_VERSION
sudo dkms autoinstall $PACKAGE_NAME/$PACKAGE_VERSION
```

In case you close your terminal before finishing the installation, you need to
run the command `source dkms.conf` to read the variables used. After finishing installing everything, you need to reboot your Jetson.

## Jetson Status - jtop command
For verifying your Jetson Nano status like CPU/GPU temperature, usage, etc. we
can download the `jetson_stats` repo that contains the `jtop` command (similar
the `htop` command on linux).
<a href="https://github.com/rbonghi/jetson_stats" target="_blank">
    Jetson Stats Github Repository
</a>

## Python Virtual Environment
For this part, we followed a guide, but only where it explains how to download
and configure the virtual environments:
<a href="https://www.pyimagesearch.com/2019/05/06/getting-started-with-the-nvidia-jetson-nano/" target="_blank">
    PyImageSearch - Getting Started With The NVIDIA Jetson Nano
</a>

To avoid having problems with the python installed in Jetson's system, we have
to make use of virtual environments. For that we install the `virtualenv` and 
`virtualenvwrapper` packages with the following command (for python3):

```
sudo pip3 install virtualenv virtualenvwrapper
```

After installed, we need to update the `.bashrc` file. For that you can use the
VIM file editor with the following command in the terminal:

```
vim ~/.bashrc
```

With the file opened, add these lines to the end:

```
# virtualenv and virtualenvwrapper
export WORKON_HOME=$HOME/.virtualenvs
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
source /usr/local/bin/virtualenvwrapper.sh
```

After saving the file and exiting the editor, reload the `.bashrc` file with
the following command:

```
source ~/.bashrc
```

With that done, we need to create our virtualenv. Also, to use all the packges
already installed in the system-wide python, which contains the OpenCV library
and such, we need to pass the flag `--system-site-packages` when creating our
environment:

```
mkvirtualenv -p python3 --system-site-packages py3env
```

In this example we named our envinonment `py3env`, but you can choose whatever
name you like. After created, we can enter the virtual environment with the
following command (again, use the name you chose for the environment):

```
workon py3nev
```

## `.bashrc` modifications
Add CUDA to path


# YOLOv5

This repository is a fork of the Ultralytics YOLOv5 repository, and its original
`README` file is the `README_yolov5.md`.
