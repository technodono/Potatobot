# Potatobot

These is the repository for practice code for potatobot.

test

#Installation

Check out <https://github.com/robotpy/pyfrc> for reference. There are a number of commands you need to run.
You need to install the pyfrc library:

    pip3 install pyfrc

If you've already installed it you should make sure you're using the latest from time to time:

    pip3 install pyfrc --upgrade

To use the joystick you need pygame. If you have hombrew on OSX, you can install it _with python3 support_ using:

    brew install pygame --with-python3

# Running in the simulator

Do this:

    python3 robot.py sim

#Deployment

To deploy the code to the robot, you need to be on the robot network and type following;

    python3 robot.py deploy

# Robot Design

* winch to pull back the elastic for firing the boulder
* limit switch to detect the position of the winch
* servo-controlled peg that holds the elastic and lets go to fire



