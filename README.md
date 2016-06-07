# Potatobot

These is the repository for code for Major Tom - for some reason it is known as *potatobot*.

# Preparation

If you already know *python 3* and *pip* you can skip this section, otherwise read on and You might be ready to start hacking on the code, but if you have not written python3 code on this platform before, you should definitely read all of this.

Before you can work on this project, you will need a few tools installed on your computer. Some may already be installed. We work extensively with *command line tools* which mean you type a command in a text area, hit enter and the command is executed. If it works, depending on the command it may print something.

On Windows this means you have to use the _Command Prompt_.

On Mac this means you have to use _Terminal_.

If you're using Linux, open a _terminal_, _shell_ or _xterm_.

If you have Python 3 installed on your computer, you can run the following included sanity check script:

On Mac (use Terminal) or Linux:

    ./sanity.py

On Windows (open a *Command Prompt* in this project directory):

    py sanity.py

Run this script to see if your computer is set up and ready to code. If _computer says no_ then read on to learn how to get the necessary tools installed.

# Installation

You have to do this stuff _once_ on your computer to make sure it is ready to work on the code.

You need to install the pyfrc library:

    pip3 install pyfrc

Have a look at out <https://github.com/robotpy/pyfrc> for detailed info on this library and how it works. 

If you installed it weeks or months ago should make sure you're using the latest from time to time:

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

## Base

* Drivetrain is 6WD tank-steering with 2x CIM motors into a 72:1 gearbox on each side driving middle wheels and toothed belts driving front and rear wheels on each side
* Each motor has an independent Vex speed controller connected directly to a RoboRIO PWM port
* usb camera (servo-mounting optional)
* 2nd usb camera 

## Game Piece

There is a basic lifter arm with a single gear motor that can be used to open the portcullis in FRC Stronghold 2016 but the encoder for this arm was not finished by the end of the build season time so the arm is very difficult to use.

The robot has very good mobility and a low profile but lacks much else in the way of finished game piece mechanisms. Here's some of our incomplete game piece components:
    

## Ball Grabber (incomplete):

    * some ball grabbing sub assembly with grabby things and something to tip the ball into the ballista (notably not
chopsticks)

## Ballista idea (incomplete):
    * winch to pull back the elastic for firing the boulder
    * limit switch to detect the position of the winch
    * servo-controlled peg that holds the elastic and lets go to fire
    * some mechanism for aiming the ballista (up and down)
    * maybe an encoder or potentiometer for measuring the tilt of the ballista



