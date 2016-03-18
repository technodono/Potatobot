'''
    This test module imports tests that come with pyfrc, and can be used
    to test basic functionality of just about any robot.
'''

from pyfrc.tests import *

from robot import MyRobot


class MockControls:
    multiplier = 1

    def get_throttle_multiplier(self):
        return self.multiplier


def test_drive():
    r = MyRobot()
    r.controls = MockControls()
    r.controls.multiplier = 1
    # full right
    l, r = r.calculate_drive(0.0, 1.0)
    assert l == 1.0 and r == 1.0

def test_drive():
    r = MyRobot()
    r.controls = MockControls()
    r.controls.multiplier = 1
    # should be straight forward (?)
    l, r = r.calculate_drive(1.0, 0.0)
    assert l == -1.0 and r == 1.0

