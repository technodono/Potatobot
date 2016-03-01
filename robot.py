# By Alex Rowell, Beniamino Briganti, Lucca Buonamano, Blake Mountford and Lex Martin

import math

import wpilib

from rigs.controls import OldControls, NewControls

#  motor port assignments
BACK_RIGHT = 0
FRONT_RIGHT = 1
BACK_LEFT = 2
FRONT_LEFT = 3
PORTCULLIS_ARM = 4

JOYSTICK_PORT = 0


# noinspection PyAttributeOutsideInit
class MyRobot(wpilib.IterativeRobot):

    def robotInit(self):  # creates all the objects needed to operate the robot
        self.pdp = wpilib.PowerDistributionPanel()
        self.leftFront = wpilib.Victor(FRONT_LEFT)
        self.leftBack = wpilib.Victor(BACK_LEFT)
        self.rightFront = wpilib.Victor(FRONT_RIGHT)
        self.rightBack = wpilib.Victor(BACK_RIGHT)

        self.portcullis_arm = wpilib.Victor(PORTCULLIS_ARM)

        try:
            self.camera = wpilib.USBCamera()
            self.camera.setExposureManual(50)
            self.camera.updateSettings()
            self.server = wpilib.CameraServer.getInstance()
            self.server.startAutomaticCapture(self.camera)
        except:
            pass

        # at the moment we are using the ps3 controller for the simulator, if we want to use the real
        # joystick we will need to change this:
        self.oldcontrols = OldControls(wpilib.Joystick(JOYSTICK_PORT))
        self.newcontrols = NewControls(wpilib.Joystick(JOYSTICK_PORT))

        self.controls = self.oldcontrols

        self.timer = wpilib.Timer()  # creates a timer to time the autonomous mode

    def disabledInit(self):
        self.logger.info("Disabled Mode")

    def testInit(self):
        self.logger.info("Test Mode")

    def calculate_drive(self, forward, turn):
        left_value = -forward + turn
        left_value *= math.fabs(left_value)
        multiplier = self.controls.get_throttle_multiplier()
        left_value *= multiplier
        right_value = -forward - turn
        right_value *= math.fabs(right_value)
        right_value *= multiplier

        return left_value, -right_value  # TODO invert the right side at the controller config level

    # drive the tank wheels according to forward and turn parameters
    def arcade_drive(self, forward, turn):
        left_value, right_value = self.calculate_drive(forward, turn)

        self.leftFront.set(left_value if self.controls.lf_toggle else 0)
        self.leftBack.set(left_value if self.controls.lb_toggle else 0)
        self.rightFront.set(right_value if self.controls.rf_toggle else 0)
        self.rightBack.set(right_value if self.controls.rb_toggle else 0)

    def autonomousInit(self):
        self.logger.info("Autonomous Mode")
        # resets and starts the timer at the beginning of autonomous
        self.timer.reset()
        self.timer.start()

    # What to do in autonomous
    def autonomousPeriodic(self):
        pass
        # commented this out for now, it's dangerous to leave it here without any modelling or testing
        # this sets up code that makes the robot drive forward for two seconds, hence the timer
        #if self.timer.get() < 2:
        #    self.arcade_drive(0.7, 0)  # sets the robot to drive forward at 0.7 of the normal speed
        #else:
        #    self.arcade_drive(0, 0)

    # What to do at the beginning of teleop
    def teleopInit(self):
        self.logger.info("Teleoperated Mode")

    # What to do continuously in teleop
    def teleopPeriodic(self):
        self.controls.update()
        self.arcade_drive(self.controls.forward(), self.controls.turn())

        if self.controls.debug_button():
            self.print_debug_stuff()

        try:
            self.camera
            exp = self.camera.exposureValue
            if self.controls.exposure_up_button() and exp < 100:
                self.camera.setExposureManual(exp + 10)
            if self.controls.exposure_down_button() and exp > 0:
                self.camera.setExposureManual(exp - 10)
        except:
            pass

        if self.controls.lift_portcullis():
            self.portcullis_arm.set(0.5)
            self.logger.debug("raising")
        elif self.controls.lower_portcullis():
            self.portcullis_arm.set(-0.5)
            self.logger.debug("lowering")
        else:
            self.portcullis_arm.set(0)


        # wpilib.SmartDashboard.putNumber("control_preset", exp)
        # preset = wpilib.SmartDashboard.getString("control_preset", "old_joystick")
        # if preset == "old_joystick" and self.controls != self.oldcontrols:
        #     self.logger.debug("switching to old controls")
        #     self.controls = self.oldcontrols
        # elif preset == "new_joystick" and self.controls != self.newcontrols:
        #     self.logger.debug("switching to new controls")
        #     self.control = self.newcontrols


    # These lines are needed to keep the motors turned off when the robot is disabled
    def disabledPeriodic(self):
        self.leftFront.set(0)
        self.leftBack.set(0)
        self.rightFront.set(0)
        self.rightBack.set(0)
        self.portcullis_arm.set(0)


    def print_debug_stuff(self):
        self.logger.info("debug stuff!!")

        try:
            # only if camera is configured
            self.camera
            self.logger.info("camera active: " + str(self.camera.active))
            self.logger.info("camera name: " + str(self.camera.name))
            self.logger.info("camera exposure: " + str(self.camera.exposureValue))
            self.logger.info("camera fps: " + str(self.camera.fps))
            self.logger.info("camera res: " + str(self.camera.width) + "x" + str(self.camera.height))
        except:
            pass


# The following lines of code are ALWAYS needed to deploy code onto the robot
if __name__ == '__main__':
    wpilib.run(MyRobot)
