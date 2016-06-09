# CamDevice
Dependencies:
install MJPG-streamer, instructions are found here: https://www.raspberrypi.org/forums/viewtopic.php?t=48597

Camdevice is a raspberry pi with a camera module and some sensors, leds, buttons and a switch.
The purpose is to act as a cam-module in a surveillance system or as a dashcam or other projects where a videostream 
is needed. An accelerometer rotates the videostream depending om the camera mounting. Leds are used for displaying 
operation mode, switch for turning videostream on/off etc.

First commit functions:
* videostream. Rotated depending on mounting
* Switch to enable/disable videostream

More info: http://www.sundback.com/wp/tag/camdevice/
 

To view stream:
sudo python Main.py

http://cam-ip:8080/?action=stream 


