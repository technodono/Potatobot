
import logging
import math

import wpilib


class Controls:

    def get_throttle_multiplier(self):
        print("override me")

    def message_test(self):
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
    MESSAGE_TEST = 4
    DEBUG_BUTTON = 7
    EXPOSURE_UP_BUTTON = 5
    EXPOSURE_DOWN_BUTTON = 6

    logger = logging.getLogger('old_controls')

    def __init__(self, joystick):
        self.stick = joystick
        self.multiplier = 1
        self.throttle_toggle = False
        self.logger.debug("old controls constructor")

    def get_throttle_multiplier(self):
        new_multiplier = (-self.stick.getThrottle() + 1) / 2
        if math.fabs(new_multiplier - self.multiplier) > 0.1:
            self.logger.info("Throttle: " + str(new_multiplier))
            wpilib.SmartDashboard.putString('throttle', str(new_multiplier))
        self.multiplier = new_multiplier
        return self.multiplier

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


