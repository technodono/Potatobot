#!/usr/bin/env python3 

import sys
import platform
from distutils.spawn import find_executable
from subprocess import PIPE, Popen
import imp
import re

MAGENTA = '\033[95m'
BLUE = '\033[94m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
NORMAL = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

def green(text):
    return GREEN + text + NORMAL

def magenta(text):
    return MAGENTA + text + NORMAL

def bold(text):
    return BOLD + text + NORMAL

def red(text):
    return RED + text + NORMAL

def fatal(result, name, instructions=""):
    if (result):
        print("checking for " + magenta(name) + " " + green(CHECK))
    else:
        print("You do not have " + magenta(name) + " installed! " + red(CROSS + " FAIL"))
        if (len(instructions) > 0):
            print(" You should " + bold(instructions))
        exit(1)

def fatalexe(name): 
    fatal(find_executable(name), name)

def format_version(i):
    return str(i.major) + "." + str(i.minor) + "." + str(i.micro)

print(green(open('scripts/logo.txt').read()))

# platform.system() -> "Windows", "Darwin" or "Linux"
mac = platform.system() == "Darwin"
windows = platform.system() == "Windows"
linux = platform.system() == "Linux"
pythonexe = "py" if windows else "python"
i = sys.version_info

if (not windows):
    CHECK='\u2714'
    CROSS='\u2716'
else:
    # unicode escapes don't work on all versions of windows
    CHECK='YES'
    CROSS='NO'


if (i.major < 3):
    print ("This is " + magenta("Python " + str(i.major)) + " but you need the latest 3.x")
    if (not windows and find_executable("python3")):
        print(" you should start this script with " + magenta("python3"))
    elif (mac and find_executable("brew")): 
        print (" you're on " + bold("\uf8ff Mac") + " and have " + magenta("brew") + " so " + green("brew install python3"))
    exit(1)
else:
    print("checking " + magenta("python") + " version: " + format_version(i) + " " + green(CHECK))

fatalexe("git")

if (mac and find_executable("brew")):
        cmd = ["brew", "list", "pygame"]
        p = Popen(cmd, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        (stdout, stderr) = p.communicate()
        p.wait()
        fatal(p.returncode == 0, "pygame", "brew install pygame --with-python3")

try:
    imp.find_module("pygame")
except ImportError:
    print(red(CROSS) + " Failed to find pygame module using imp")
            
# TODO check if pygame is installed from windows

modules = set(["pyfrc", "wpilib"])

# now test python modules
for module in modules:
    try:
        imp.find_module(module)
        print("checking python module " + magenta(module) + " " + green(CHECK))
    except ImportError:
        if (find_executable("pip3")):
            fatal(False, module, "pip3 install " + module)
        else:
            fatal(False, module, pythonexe + " -m pip install " + module)

# check git remote just in case somebody has the old one
p = Popen(['git', 'config', '--get', 'remote.origin.url'], stderr=PIPE, stdout=PIPE, universal_newlines=True)
p.wait()
if (p.returncode == 0):
    stdout, stderr = p.communicate()
    p = re.compile('(git@|https://)github.com(/|:)rIGS2016/')
    if (p.match(stdout)):
        print("Yo code poet, you have the " + bold("old remote repo. ") + red(CROSS))
        print("You need to run this:")
        print()
        print(green(" git remote set-url origin git@github.com:rIGSteam/Potatobot.git"))
        print()
        exit(1)

print()
print(bold("Everything looks good, let's go write some robot code"))
print()

