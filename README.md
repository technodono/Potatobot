﻿# Potatobot

These is the repository for practice code for potatobot.


# Installation

Check out <https://github.com/robotpy/pyfrc> for reference. There are a number of commands you need to run.
You need to install the pyfrc library:

    pip3 install pyfrc

If you've already installed it you should make sure you're using the latest from time to time:

    pip3 install pyfrc --upgrade

To use the joystick you need pygame. If you have hombrew on OSX, you can install it _with python3 support_ using:

    brew install pygame --with-python3

# Run the tests!

The best way to see if things work is by running the tests. Here's how:

    python3 robot.py test

If there are any failures or error messages, you are not good to push nor should you expect the robot or even the simulator to work 

# Running in the simulator

Do this:

    python3 robot.py sim

The ```config.json``` file specifies the field used in the simulator. Note that the colours used come from the
tkinter library and are enumerated here: <http://wiki.tcl.tk/37701>

# Deployment

To deploy the code to the robot, you need to be on the robot network and type following;

    python3 robot.py deploy

# Robot Design

* winch to pull back the elastic for firing the boulder
* limit switch to detect the position of the winch
* servo-controlled peg that holds the elastic and lets go to fire
* usb camera
* some mechanism for aiming the ballista (up and down)
* maybe an encoder or potentiometer for measuring the tilt of the ballista
* some ball grabbing sub assembly with grabby things and something to tip the ball into the ballista (notably not
chopsticks)



