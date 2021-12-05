# Introduction
This repository contains the code used in our undergraduate's final assignment
(TCC - Trabalho de Conclusão de Curso, in portuguese) to obtain the title of
Mechatronics Engineers by the Escola Politécnia, Universidade de São Paulo (EP-USP).

Authors: Erick Sun and Rodrigo Heira Akamine

#### Examples:

Example of reduction of velocity when seeing a "person":

![Alt Text](./assets/reduz_Trim.gif)

Example of stopping the robot when seeing a "person":

![Alt Text](./assets/parar_Trim.gif)

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
- Phone charger and micro-usb or barrel jack cable
- For use with a "mobile" power source, and with heavy usage of CPU/GPU, it is
recommended to power your Jetson through the barrel jack and a reliable power bank
	- In our case, it was used the Baseus Adaman Metal Digital Display - Quick
	Charge Power Bank - 10000mAh - 22.5W
	- With this, the voltage supply didn't oscilate bellow 4.75V that is the Jetson's
	minimum voltage to operate. Bellow this value, it will start to malfunction
	and maybe even turn off.

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

## First boot
With the microSD card flashed, plug it in your Jetson, connect the HDMI cable,
mouse, keyboard, wifi adapter and ethernet cable and power it up. With this you
should see it boot up and load the Ubuntu. Next we need to install the necessary
drivers for the wifi adapter.

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
run the command `source dkms.conf` to read the variables used. After finishing
installing everything, you need to reboot your Jetson.

Done that, you can connect to your wifi network, and with that, you will be able
to connect to your Jetson through a `ssh` connection.

## SSH Connect to Jetson
With your Jetson connected to your network, you can run the following commands
on your own computer to find the Jetson's IP address:

```
# If you don't have nmap installed
sudo apt update
sudo apt install nmap

# Verify your network's IP address
ifconfig

# Now you should see a line like: inet 192.168.XX.XX
# Just scan your network for the IP address your Jetson is using
# Don't forget to change the XX for your network's numbers
nmap -sn 192.168.XX.0/24  # or nmap -sL 192.168.XX.0/24

# You should see one written with "jetbot" or "edimax ..."
# Just copy that IP address and connect to it with ssh
# And enter the password to the user
ssh <user>@<IP address found>

# If you set the user to 'jetbot' and password to 'jetbot'
ssh jetbot@<IP address found>
>>> Enter jetbot's password: jetbot [ENTER]
```

Another way would be to verify the Jetson's IP address inside it. Just open a terminal
and type: `ifconfig`. You should see it's IP address, and to know the user's name
just type `whoami`. Then in your own computer, just connect to your Jetson through
`ssh`.

## Jetson's Power Modes and Jetson Clocks
If you are using a weaker power supply and/or micro-usb, consider turning your
Jetson to `5W mode`. In case you have a better and more stable power supply
you may use the `10W mode` and maybe use the overclock with the `jetson_clocks`
command.

```
# Verify which mode is in use
sudo nvpmodel -q

# Change to 5W mode
sudo nvpmodel -m 1

# Change to 10W mode
sudo nvpmodel -m 0

# Use jetson_clocks
sudo jetson_clocks
```

By default, Jetson uses `10W mode`, and the `jetson_clocks` turns off automatically
when you reboot. These modes and the `jetson_clocks` can also be verified with
the `jtop` command, which can be installed by following the steps in the next section.

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

### OpenCV import error in virtual environment:
If it returns an error when you run a `import cv2` inside your virtual environment,
we need to create a `symlink` from the OpenCV library installed to your virtual
environment's import path with the following commands:

```
ln -s /usr/lib/python3.6/dist-packages/cv2/python-3.6/cv2.cpython-36m-aarch64-linux-gnu.so /home/jetbot/.virtualenvs/<your_env>/lib/python3.6/site-packages/cv2.cpython-36m-aarch64-linux-gnu.so
```

In case you can't find the library path, you can find it with the following way:

```
# Deactivate the virtual environment
deactivate

# Enter python command line
python3

# Type in the following commands
>>> import cv2
>>> print(cv2.__file__)
```

With the final command, if it succesfully imported the OpenCV library, it should
print out it's file path, and with that you can create the `symlink`:

```
ln -s <file path> /home/jetbot/.virtualenvs/<your_env>/lib/python3.6/<file_name>
```

After that, you should be able to `import cv2` inside your virtual environment.

## Use Jetson CSI Camera
To use the CSI camera with Jetson in OpenCV, we need to pass a command to the
`cv2.VideoCapture()` function.

Inside the file `simple_camera.py` you can find a function that returns the command
used to instantiate the camera. To open it, just pass the `command` as:

```python
cap = cv2.VideoCapture(command, cv2.CAP_GSTREAMER)

# Verify if it worked
print(cap.isOpened())  # Returns True if it worked
```

**OBS:** If the Jetson is **NOT** connected to a monitor through HDMI, the function
`cv2.imshow()` **WILL NOT WORK**, and it will either throw an error in your script
or reset your jupyter notebook/lab kernel. To see the image, you can either connect
your Jetson to a monitor, or inside your jupyter notebook/lab, use the
`IPython.display` class.

```python
import cv2
from IPython.display import display, Image

# Open cv2.VideoCapture routine: start
...
# end

# Display handle in a separate cell
display_handle = display(None, display_id=True)

# You can put this part in a loop if you want
_, image = camera.read()
_, image = cv2.imencode('.jpeg', image)
display_handle.update(Image(data=image.tobytes()))
```

## Jupyter Lab/Notebooks
For easier file navigation and code testing, you can install `jupyter lab` and
or `jupyter notebook` with the following command:

```
workon <your env>
pip install jupyterlab notebook
```

Firstly, generate jupyter's configuration file:

```
jupyter notebook --generate-config
```

And the we can define the password with the following command:

```
jupyter notebook password
```

To open a server so you can access it on your own computer, run the command:

```
# For jupyter notebook
jupyter notebook --no-browser --ip=0.0.0.0 --port=8888

# For jupyter lab
jupyter lab --no-browser --ip=0.0.0.0 --port=8888
```

Then you can access it by typing `<Jetson's IP Address>:8888` in your computer's
browser.

## `.bash_aliases` for easy access
In your Jetson Nano there will probably exist a file called `~/.bash_aliases`
that is imported inside your `~/.bashrc` file. In this file you can create `aliases`
so you don't need to type big lines of commands all the time.

Next we will show an example that we used:

```
alias py3="workon py3"
alias jlb="py3 && jupyter lab --no-browser --ip=0.0.0.0 --port=8888"
alias restart_cam="sudo systemctl restart nvargus-daemon"
```

The `restart_cam` was used to restart the `nvargus-daemon` service used to initialize
Jetson's camera

## `.bashrc` modifications
Add these lines to the end of your `~/.bashrc` file so it can find CUDA and resolve
some problems with the architecture:

```
# CUDA
export PATH=/usr/local/cuda/bin${PATH:+:${PATH}}
export LD_LIBRARY_PATH=/usr/local/cuda/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}

export OPENBLAS_CORETYPE=AARCH64
export LD_PRELOAD=/usr/lib/aarch64-linux-gnu/libgomp.so.1
```

After you've added these lines, run a `source ~/.bashrc` and you will be able to
verify your CUDA version with the following command (or using `jtop`):

```
nvcc --version
```

## Installing PyTorch and TorchVision

To install PyTorch, download the `wheel` for the desired version in
<a href='https://forums.developer.nvidia.com/t/pytorch-for-jetson-version-1-10-now-available/72048' target='_blank'>
this link
</a>
and follow the instructions for your CUDA, JetPack and Python version, and to install the according
torchvision. For this project, we used the `PyTorch v1.9` and `torchvision v0.10.0`.

You can also verify which PyTorch version is compatible with your CUDA in
<a href='https://pytorch.org/get-started/previous-versions/' target='_blank'>
this link.
</a>

## Installing QWIIC Libraries and Sparkfun's JetBot

To use the Sparkfun motor drivers, you need to install their libraries with the
following command:

```
workon <your virtual environment>
pip install sparkfun-qwiic
```

After that, there is a repository of theirs that is a fork from NVIDIA's original
JetBot repo that is adapted to work with their motors. To install it, run the
following commands:

```
workon <your virtual environment>
cd ~
git clone https://github.com/sparkfun/jetbot
cd jetbot && python setup.py install
```

## Turn GNOME's graphical interface off
If you're in need of every bit of memory, you can turn the graphical interface
that can consume more than 1GB of memory off with the following command (in case
you're already connecting to your Jetson through SSH only):

```
# To turn the graphical interface off
sudo systemctl set-default multi-user.target

# To turn it back on
sudo systemctl set-default graphical.target
```

After running the command, reboot.

## NVIDIA's TensorRT and Torch2TRT
For better performance of your models, you can use NVIDIA's TensorRT, and NVIDIA's
package Torch2TRT to convert your models. In this section it is explained how to
`import` and install the package, but we were not able to effectively use it in
our final model due to time.

NVIDIA's TensorRT already comes installed with the JetPack SDK, to make it visible
inside your virtual environment, we need to follow a similar process as in to import
the OpenCV library steps done previously.

First, we can verify how it is imported by the system's python:

```
# Enter system python
deactivate
python3

# Import tensorrt and print its path
>>> import tensorrt as trt
>>> print(trt.__file__)
```

It will probably print something like `/usr/lib/python3.6/dit-packages/tensorrt/__init__.py`,
so we need to create a `symlink` of the `tensorrt` folder to our virtual environment's 
import path:

```
ln -s /usr/lib/python3.6/dist-packages/tensorrt /home/jetbot/.virtualenvs/<your_env>/lib/python3.6/site-packages/tensorrt
```

With this, you should be able to `import tensorrt` inside your virtual environment.

After this, we can install NVIDIA's `torch2trt` which is a PyTorch to TensorRT
converter, following their GitHub's repository:
<a href='https://github.com/NVIDIA-AI-IOT/torch2trt' target='_blank'>
NVIDIA-AI-IOT/torch2trt
</a>

```
workon <your env>
git clone https://github.com/NVIDIA-AI-IOT/torch2trt
cd torch2trt
python setup.py install
```

# YOLOv5

This repository is a fork of the Ultralytics YOLOv5 repository, and its original
`README` file is the `README_yolov5.md`.
