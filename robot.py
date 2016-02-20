# By Alex Rowell, Beniamino Briganti, Lucca Buonamano, Blake Mountford and Lex Martin

import wpilib
import math

from rigs.controls import OldControls

#  motor port assignments
BACK_RIGHT = 0
FRONT_RIGHT = 1
BACK_LEFT = 2
FRONT_LEFT = 3
GAME_ARM = 4


CAMERA_SERVO = 5  # PWM
JOYSTICK_PORT = 0


# noinspection PyAttributeOutsideInit
class MyRobot(wpilib.IterativeRobot):

    def robotInit(self):  # creates all the objects needed to operate the robot
        self.pdp = wpilib.PowerDistributionPanel()
        self.leftFront = wpilib.VictorSP(FRONT_LEFT)
        self.leftBack = wpilib.VictorSP(BACK_LEFT)
        self.rightFront = wpilib.VictorSP(FRONT_RIGHT)
        self.rightBack = wpilib.VictorSP(BACK_RIGHT)
        self.camera_pan = wpilib.Servo(CAMERA_SERVO)
        self.game_arm = wpilib.VictorSP(GAME_ARM)
        self.camera = wpilib.USBCamera()
        self.camera.setExposureManual(50)
        # self.camera.setBrightness(80)
        self.camera.updateSettings()

        server = wpilib.CameraServer.getInstance()
        server.startAutomaticCapture(self.camera)
        # at the moment we are using the ps3 controller for the simulator, if we want to use the real
        # joystick we will need to change this:
        self.controls = OldControls(wpilib.Joystick(JOYSTICK_PORT))

        # if self.isReal():
        #     self.controls = OldControls(wpilib.Joystick(JOYSTICK_PORT), self.logger)
        # else:
        #     self.controls = PS3Controls(wpilib.Joystick(JOYSTICK_PORT), self.logger)

        self.leftFront = wpilib.VictorSP(FRONT_LEFT)
        self.leftBack = wpilib.VictorSP(BACK_LEFT)
        self.rightFront = wpilib.VictorSP(FRONT_RIGHT)
        self.rightBack = wpilib.VictorSP(BACK_RIGHT)
        self.camera_pan = wpilib.Servo(CAMERA_SERVO)
        self.camera = wpilib.USBCamera()
        self.camera.setExposureManual(50)
        # self.camera.setBrightness(80)
        self.camera.updateSettings()

        server = wpilib.CameraServer.getInstance()
        server.startAutomaticCapture(self.camera)
        # at the moment we are using the ps3 controller for the simulator, if we want to use the real
        # joystick we will need to change this:
        self.controls = OldControls(wpilib.Joystick(JOYSTICK_PORT))

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
        self.logger.error("Log test")
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


    # The following lines tell the robot what to do in teleop
    def teleopPeriodic(self):
        self.arcade_drive(self.controls.forward(), self.controls.turn())

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
        self.firing_pin.setAngle(RELEASE_DEGREES)  # TODO no idea what angle this should be right now

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

# By Alex Rowell, Beniamino Briganti, Lucca Buonamano, Blake Mountford and Lex Martin
