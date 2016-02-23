# By Alex Rowell, Beniamino Briganti, Lucca Buonamano, Blake Mountford and Lex Martin

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
    MESSAGE_TEST = 8
    DEBUG_BUTTON = 7
    EXPOSURE_UP_BUTTON = 12
    EXPOSURE_DOWN_BUTTON = 11
    TRIGGER = 1
    THUMB_BUTTON = 2

    TOGGLE_LB = 3
    TOGGLE_RB = 4
    TOGGLE_LF = 5
    TOGGLE_RF = 6

    logger = logging.getLogger('old_controls')

    def __init__(self, joystick):
        self.stick = joystick
        self.multiplier = 1
        # motors can be disabled with these:
        self.lf_toggle = True
        self.toggle_listen = 0.0
        self.lb_toggle = True
        self.rf_toggle = True
        self.rb_toggle = True
        self.logger.debug("old controls constructor")
        self.timer = wpilib.Timer()
        self.timer.reset()
        self.timer.start()

    def get_throttle_multiplier(self):
        new_multiplier = (-self.stick.getThrottle() + 1) / 2
        diff = math.fabs(new_multiplier - self.multiplier)
        if diff > 0.1:
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

    def lift_portcullis(self):
        return self.stick.getRawButton(self.TRIGGER)

    def lower_portcullis(self):
        return self.stick.getRawButton(self.THUMB_BUTTON)

    def grabber(self):
        return self.stick.getX()

    def update(self):

        if self.stick.getRawButton(self.TOGGLE_RF) and self.toggle_listen < self.timer.get():
            self.rf_toggle = not self.rf_toggle
            self.logger.info("Right Front Motor %s" % self.rf_toggle)
            self.toggle_listen = self.timer.get() + 1
        if self.stick.getRawButton(self.TOGGLE_LF) and self.toggle_listen < self.timer.get():
            self.lf_toggle = not self.lf_toggle
            self.logger.info("Left Front Motor %s" % self.lf_toggle)
            self.toggle_listen = self.timer.get() + 1
        if self.stick.getRawButton(self.TOGGLE_RB) and self.toggle_listen < self.timer.get():
            self.rb_toggle = not self.rb_toggle
            self.logger.info("Right Back Motor %s" % self.rb_toggle)
            self.toggle_listen = self.timer.get() + 1
        if self.stick.getRawButton(self.TOGGLE_LB) and self.toggle_listen < self.timer.get():
            self.lb_toggle = not self.lb_toggle
            self.logger.info("Left Back Motor %s" % self.lb_toggle)
            self.toggle_listen = self.timer.get() + 1


# TODO ps3 controls, keyboard controls and alternate joystick controls
class NewControls(Controls):

    MESSAGE_TEST = 4
    DEBUG_BUTTON = 7
    EXPOSURE_UP_BUTTON = 5
    EXPOSURE_DOWN_BUTTON = 6

    logger = logging.getLogger('new_controls')

    def __init__(self, joystick):
        self.stick = joystick
        self.multiplier = 1
        self.throttle_toggle = False

    def get_throttle_multiplier(self):
        new_multiplier = (-self.stick.getThrottle() + 1) / 2
        if math.fabs(new_multiplier - self.multiplier) > 0.1:
            self.logger.info("Throttle: " + str(new_multiplier))
            wpilib.SmartDashboard.putString('/SmartDashboard/throttle', str(new_multiplier))
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
        return self.stick.getX()
