# By Alex Rowell, Beniamino Briganti, Lucca Buonamano, Blake Mountford and Lex Martin

import wpilib
import math
import smart_dashboard_test

#  port assignments
from smart_dashboard_test import Smart_Dashboard_Test

MOTOR1_PWM = 0
MOTOR2_PWM = 1
MOTOR3_PWM = 2
MOTOR4_PWM = 3

BACK_RIGHT = 0
FRONT_RIGHT = 1
BACK_LEFT = 2
FRONT_LEFT = 3
FIRING_SERVO = 4  # PWM
CAMERA_SERVO = 5  # PWM
JOYSTICK_PORT = 0
FIRING_WINCH_LIMIT_SWITCH_CHANNEL = 0

# firing pin positions TODO: no idea what angle these should be right now
HOLD_DEGREES = 0
RELEASE_DEGREES = 180


class Controls:

    def get_throttle_multiplier(self):
        print("override me")

    def update_throttle(self):
        print("override me")

    def reset_firing_pin_button(self):
        print("override me")

    def fire_button(self):
        print("override me")

    def debug_button(self):
        print("override me")

    def get_camera_position(self):
        print("override me")

    def exposure_up_button(self):
        print("override me")

    def exposure_down_button(self):
        print("override me")

    def forward(self):
        print("override me")

    def turn(self):
        print("override me")


class OldControls(Controls):

    # Joystick Buttons
    THROTTLE_TOGGLE = 4
    NORMAL_THROTTLE = 2
    THIRTY_FIVE_PERCENT_THROTTLE = 3
    DOUBLE_THROTTLE = 5
    FIRING_SERVO_RESET_BUTTON = 8
    DEBUG_BUTTON = 7
    EXPOSURE_UP_BUTTON = 11
    EXPOSURE_DOWN_BUTTON = 12

    def __init__(self, joystick, logger):
        self.stick = joystick
        self.multiplier = 1
        self.throttle_toggle = False
        self.logger = logger

    def get_throttle_multiplier(self):
        return self.multiplier

    def update_throttle(self):
        if self.stick.getRawButton(self.DOUBLE_THROTTLE):
            self.multiplier = 2
            self.throttle_toggle = False
        if self.stick.getRawButton(self.NORMAL_THROTTLE):
            self.multiplier = 1
            self.throttle_toggle = False
        if self.stick.getRawButton(self.THIRTY_FIVE_PERCENT_THROTTLE):
            self.multiplier = 0.35
            self.throttle_toggle = False
        if self.stick.getRawButton(self.THROTTLE_TOGGLE):
            self.throttle_toggle = True
        if self.throttle_toggle:
            new_multiplier = (-self.stick.getThrottle() + 1) / 2
            if not new_multiplier == self.multiplier:
                self.logger.debug("Throttle: " + str(new_multiplier))
            self.multiplier = new_multiplier

    def reset_firing_pin_button(self):
        return self.stick.getRawButton(self.FIRING_SERVO_RESET_BUTTON)

    def fire_button(self):
        return self.stick.getTrigger()

    def debug_button(self):
        return self.stick.getRawButton(self.DEBUG_BUTTON)

    def get_camera_position(self):
        return self.stick.getX()

    def exposure_up_button(self):
        return self.stick.getRawButton(self.EXPOSURE_UP_BUTTON)

    def exposure_down_button(self):
        return self.stick.getRawButton(self.EXPOSURE_DOWN_BUTTON)

    def message_test(self):
        return self.stick.getRawButton(self.MESSAGE_TEST)

    def forward(self):
        return self.stick.getY()

    def turn(self):
        return self.stick.getZ()


# TODO ps3 controls, keyboard controls and alternate joystick controls
class PS3Controls(OldControls):

    def turn(self):
        turn_amount = super(PS3Controls, self).turn()
        self.logger.debug("turn amount: " + str(turn_amount))
        return turn_amount


# noinspection PyAttributeOutsideInit
class MyRobot(wpilib.IterativeRobot):

    def robotInit(self):  # creates all the objects needed to operate the robot
        self.pdp = wpilib.PowerDistributionPanel()
        self.leftFront = wpilib.VictorSP(FRONT_LEFT)
        self.leftBack = wpilib.VictorSP(BACK_LEFT)
        self.rightFront = wpilib.VictorSP(FRONT_RIGHT)
        self.rightBack = wpilib.VictorSP(BACK_RIGHT)
        self.firing_pin = wpilib.Servo(FIRING_SERVO)
        self.camera_pan = wpilib.Servo(CAMERA_SERVO)
        self.limit_switch = wpilib.DigitalInput(FIRING_WINCH_LIMIT_SWITCH_CHANNEL)
        self.camera = wpilib.USBCamera()
        self.camera.setExposureManual(50)
        # self.camera.setBrightness(80)
        self.camera.updateSettings()

        server = wpilib.CameraServer.getInstance()
        server.startAutomaticCapture(self.camera)
        # at the moment we are using the ps3 controller for the simulator, if we want to use the real
        # joystick we will need to change this:
        self.controls = OldControls(wpilib.Joystick(JOYSTICK_PORT), self.logger)

        # if self.isReal():
        #     self.controls = OldControls(wpilib.Joystick(JOYSTICK_PORT), self.logger)
        # else:
        #     self.controls = PS3Controls(wpilib.Joystick(JOYSTICK_PORT), self.logger)

        self.timer = wpilib.Timer()  # creates a timer to time the autonomous mode

    def disabledInit(self):
        self.logger.info("Disabled Mode")

    def testInit(self):
        self.logger.info("Test Mode")

    # The following lines define the arcade drive settings
    def arcade_drive(self, forward, turn):
        # use a parabolic throttle response profile
        soft_turn = turn * turn
        if turn < 0:
            soft_turn = -soft_turn
        left_value = -forward + soft_turn
        left_value *= math.fabs(left_value)
        multiplier = self.controls.get_throttle_multiplier()
        left_value *= multiplier
        right_value = -forward - soft_turn
        right_value *= math.fabs(right_value)
        right_value *= multiplier
        self.leftFront.set(left_value)
        self.leftBack.set(left_value)
        self.rightFront.set(-right_value)
        self.rightBack.set(-right_value)

    def autonomousInit(self):
        self.logger.info("Autonomous Mode")
        # resets and starts the timer at the beginning of autonomous
        self.timer.reset()
        self.timer.start()

    # The following lines tell the robot what to do in autonomous
    def autonomousPeriodic(self):
        # this sets up code that makes the robot drive forward for two seconds, hence the timer
        if self.timer.get() < 2:
            self.arcade_drive(0.7, 0)  # sets the robot to drive forward at 0.7 of the normal speed
        else:
            self.arcade_drive(0, 0)

    # The following lines tell the robot what to do in teleop
    def teleopInit(self):
        self.logger.info("Teleoperated Mode")
        try:
            sdt = Smart_Dashboard_Test()
            sdt.smart_dashboard_test(self.timer)
        except:
            self.logger.debug("smart dashboard test failed (never mind)")

    # The following lines tell the robot what to do in teleop
    def teleopPeriodic(self):
        self.arcade_drive(self.controls.forward(), self.controls.turn())
        self.controls.update_throttle()
        if self.controls.fire_button():
            self.fire()
        # for now use a reset button on the stick, later, decide when we want the pin to be engaged
        if self.controls.reset_firing_pin_button():
            self.reset_firing_pin()
        if self.limit_switch.get():
            self.logger.info("Limit switch activated")
            # TODO stop the winch (and reset the firing pin probably)
        if self.controls.debug_button():
            self.print_debug_stuff()
        self.camera_position(self.controls.get_camera_position())

        exp = self.camera.exposureValue
        if self.controls.exposure_up_button() and exp < 100:
            self.camera.setExposureManual(exp + 10)
        if self.controls.exposure_down_button() and exp > 0:
            self.camera.setExposureManual(exp - 10)

    # These lines are needed to keep the motors turned off when the robot is disabled
    def disabledPeriodic(self):
        self.leftFront.set(0)
        self.leftBack.set(0)
        self.rightFront.set(0)
        self.rightBack.set(0)

    def fire(self):
        self.logger.info("Firing...")
        self.firing_pin.setAngle(RELEASE_DEGREES)

    def reset_firing_pin(self):
        self.logger.info("Resetting...")
        self.firing_pin.setAngle(HOLD_DEGREES)

    def print_debug_stuff(self):
        try:
            self.logger.info("debug stuff!!")
            self.logger.info("camera active: " + str(self.camera.active))
            self.logger.info("camera name: " + str(self.camera.name))
            self.logger.info("camera exposure: " + str(self.camera.exposureValue))
            self.logger.info("camera fps: " + str(self.camera.fps))
            self.logger.info("camera res: " + str(self.camera.width) + "x" + str(self.camera.height))
        except:
            self.logger.error("error trying to print debug !!")

    def camera_position(self, direction):
        """
        Points the camera in a left/right direction.
        :param direction: float between -1 (left) and 1 (right) with 0 being straight ahead
        :return:
        """
        self.camera_pan.setAngle((direction + 1) * 90.0)


# The following lines of code are ALWAYS needed to deploy code onto the robot
if __name__ == '__main__':
    wpilib.run(MyRobot)

