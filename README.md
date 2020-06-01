# LEGO Facial Recognition Box

## 1. Overview

I built a LEGO box around a Raspberry Pi 3A+, it's power source, a Pi camera and a servomotor. The box can be used to keep small valuable items (e.g. wedding ring), and will only open if it detects and recognizes faces that I've saved to the database.

<img src='images/iso_main.jpg' width='500'><br>
*Presenting... the finished product.*

`Insert video here`

Of course, being built out of LEGO, a would-be thief could just dismantle the box... hehe! Still, this was a fun project and my first foray into combining LEGO with AI.

This project draws from the disciplines of mechanical, electronic and software engineering. The rest of this post explains how the box works and also some of the design decisions I've made. You may use the table of contents below to skip ahead if you'd like. Enjoy!

**Table of Contents**
- [Mechanical](#2-mechanical)
    - [Aesthetics](#21-aesthetics)
    - [Opening Mechanism](#22-opening-mechanism)
    - [Serviceability](#23-serviceability)
- [Electronics](#3-electronics)
    - [Component Selection](#31-component-selection)
    - [Wiring](#32-wiring)
    - [Servomotor Calibration](#33-servomotor-calibration)
- [Software](#4-software)
    - [Installation and Setup](#41-installation-and-setup)
    - [Running the Program](#42-running-the-program)
    - [Facial Recognition: Under the Hood](#43-facial-recognition-under-the-hood)

## 2 Mechanical

### 2.1 Aesthetics

My goal was to design the box to be compact enough to fit in the palm of my hand, which was a challenge because of all the electronics required. The only external electronic component is the camera, which I mounted on one side of the box, and hid under the golden circular bricks. Sometimes, I'm reminded of Iron Man's chestplate when I see this...

<img src='images/iso_palm.jpg' width='500'><br>
*The box encapsulates all the electronics, yet manages to be small enough to fit in the palm of my hand.*

I wanted to build something Oriental-looking this time, and decided to go with red as the main colour, with a dash of gold and brown.  I added gold [Asian window screens](https://www.bricklink.com/v2/catalog/catalogitem.page?P=32932&idColor=115#T=C&C=115) on the other three sides of the box to accentuate the Oriental look. 

![](images/iso_open.jpg)<br>
*The gold Asian window screens accentuate the Oriental look.*

`Insert ring image here`

### 2.2 Opening Mechanism

The main mechanical feature of this project is the opening and closing of the box. The objective was for a single servomotor to open and close both covers simultaneously. I tried different gear layouts and [four-bar linkages](https://hackaday.com/2017/03/29/marvelous-mechanisms-the-ubiquitous-four-bar-linkage/), and decided to go with the bevel gear mechanism shown in the animation below. Here, I've uncoupled the bevel gear from the servo, and manually rotated the shaft to illustrate how it works.

<img src='images/bevel_gear.gif' width=500><br>
*Animation of the bevel gear opening mechanism.*

The advantages of this solution are:
- The servo and geartrain can be placed within space constraints.
- Minimal freeplay of covers. If freeplay were present, even if the covers were shut, you would be able to pry them open slightly - definitely undesirable for this project. To minimise freeplay in LEGO gears, the trick is to minimise the number of gears used, therefore reducing gear [backlash](https://en.wikipedia.org/wiki/Backlash_(engineering)).

### 2.3 Serviceability

To avoid having to dismantle the box in order to charge the battery, or to do troubleshooting, I added removable panels on 4 sides of the box. The panels serve mainly aesthetic purposes, and once removed, the ports of the Raspberry Pi and HAT are exposed as shown below:

| | |
| ---| ---|
| On/off switch on the battery HAT. |<img src='images/on_off.jpg'>|
| USB Mini-B charging port, HDMI port, and camera. |<img src='images/charge_port.jpg'>|
| USB-A port.  |<img src='images/usb.jpg'>|

## 3 Electronics

### 3.1 Component Selection

What was the main factor in selecting electronic components? SPACE!!! I wanted everything to be contained within the box, while keeping the overall dimensions of the box as petite as possible. I was also adamant that the cross-section of the box should be a square instead of a rectangle (this would look weird). 

<img src='images/electronics2.jpg' width=500> <br>
*The electronics, contained within the LEGO box.*

<img src='images/electronics.jpg' width=500><br>
*The 5 main electronic components.*

The design choices for these components are summarised in the table below:

| Component | Manufacturer/Model | Rationale for Choice|
|--- |--- |--- |
| Computer | Raspberry Pi 3 Model A+ | I used a Pi 3 Model B+ initially, but changed to Model A+ because of it's smaller size and square shape. It only has 512MB of RAM compared to 1GB in the B+, but it did not seem to adversely affect performance. |
| Servomotor | LOBOT LGS-01 Micro Anti-block Servo 270° Rotation | The main requirement was that the servo had to be able to inferface with LEGO bricks. Once I found one that could, I ordered it and designed the rest of the box around it. |
| Camera | Raspberry Pi Camera Module v2 | A straightforward choice, with the added bonus that it connects to the Pi via a compact ribbon cable. |
| Battery | [WaveShare HAT-LI-01](https://sg.cytron.io/waveshare/p-li-ion-battery-hat-for-raspberry-pi-5v-output-quick-charge?src=brand) (Li-Ion Battery HAT) + Generic 14500 Li-Ion rechargeable battery | This was tricky - I really wanted the box to be portable and thus it had to have its own power source. However, most powerbanks were too bulky to fit in the box. This component fit the bill nicely, with the only downside being having to recharge it every half an hour. |
| USB Micro-B to Mini-B adapter | Generic | Connects to the battery HAT, and juts out to the edge of the box. This allows the battery to be recharged by connecting a USB Mini-B cable, without having to dismantle the box to reach the HAT. |

### 3.2 Wiring

The wiring is pretty straightforward. First, attach the battery HAT on the Raspberry Pi. Next, connect the servo to 3 GPIO pins of the HAT (as the HAT has encapsulated the Pi's pins) following this [guide](https://tutorials-raspberrypi.com/raspberry-pi-servo-motor-control/). Lastly, connect the ribbon cable of the Pi camera to the Raspberry Pi's CSI port. That's it!

### 3.3 Servomotor Calibration

`To be updated`


## 4 Software


### 4.1 Installation and Setup

This section explains how to install the required libraries on the Raspberry Pi. Basic knowledge of using Raspberry Pi such as flashing the Raspbian OS is assumed. Do note that some of the following installation steps can be time consuming.

1. Follow Adrian Rosebrock's [guide](https://www.pyimagesearch.com/2017/09/04/raspbian-stretch-install-opencv-3-python-on-your-raspberry-pi/) to:
    - Install *pip*
    - Create a virtual environment (called *cv* in our case)
    - Install *numpy*
    - Build and install *OpenCV* from source (this will take a few hours)


2. Run the following commands in a terminal.
    ```
    workon <virtual env name>
    pip install dlib
    pip install face_recognition
    pip install PyYAML
    pip install "camerapi[array]"
    pip install RPi.GPIO
    ```
    - *dlib* contains the core facial recognition functionalities
    - *face_recognition* is built on top of *dlib*, and makes it simpler to use
    - *PyYAML* allows the reading of the *settings.yml* file
    - *"camerapi[array]"* allows the Raspberry Pi camera to be used 
    - *RPi.GPIO* allows the Raspberry Pi to control the servomotor using GPIO pins

### 4.2 Running the Program

`To be updated`

### 4.3 Facial Recognition: Under the Hood

`To be updated`
