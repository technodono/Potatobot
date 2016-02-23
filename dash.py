
from __future__ import print_function

from networktables import NetworkTable
from networktables.util import ChooserControl

import sys
import time

import logging
logging.basicConfig(level=logging.DEBUG)

NetworkTable.setIPAddress("127.0.0.1")
NetworkTable.setClientMode()
NetworkTable.initialize()

def foo(value):
    print("foo", value)

def bar(value):
    print("bar", value)

def valueChanged(key, value, isNew):
    print("valueChanged: %s = %s" % (key, value) )

NetworkTable.addGlobalListener(valueChanged)

cc = ChooserControl("control_preset",
                    foo,
                    bar)
sd = NetworkTable.getTable("SmartDashboard")

while True:
    time.sleep(5)
    sd.putString("control_preset", "old_joystick")
    time.sleep(5)
    sd.putString("control_preset",4 "new_joystick")