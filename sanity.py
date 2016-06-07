#!/usr/bin/env python3 

import sys
import platform
from distutils.spawn import find_executable
from subprocess import PIPE, run
import imp
import re

# platform.system() -> "Windows", "Darwin" or "Linux"
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
        print("checking for " + magenta(name) + " " + green("✔"))
    else:
        print("You do not have " + magenta(name) + " installed! " + red("✖ FAIL"))
        if (len(instructions) > 0):
            print(" You should " + bold(instructions))
        exit(1)

def fatalexe(name): 
    fatal(find_executable(name), name)

def format_version():
    i = sys.version_info
    return str(i.major) + "." + str(i.minor) + "." + str(i.micro)

print(green(open('scripts/logo.txt').read()))

mac = platform.system() == "Darwin"
windows = platform.system() == "Windows"
linux = platform.system() == "Linux"

if (sys.version_info.major < 3):
    print ("This is " + magenta("Python " + str(sys.version_info.major)) + " but you need the latest 3.x")
    if (not windows and find_executable("python3")):
        print(" you should start this script with " + magenta("python3"))
    elif (mac and find_executable("brew")): 
        print (" you're on " + bold("") + " and have " + magenta("brew") + " so " + green("brew install python3"))
    exit(1)
else:
    print("checking " + magenta("python") + " version: " + format_version() + " " + green("✔"))

fatalexe("git")

if (mac): 
    if (find_executable("brew")):
        result = run(["brew", "list", "pygame"], stdout=PIPE, stderr=PIPE, universal_newlines=True)
        fatal(result.returncode == 0, "pygame", "brew install pygame --with-python3")
            
# TODO check if pygame is installed from windows

modules = set(["pyfrc", "wpilib"])

# now test python modules
for module in modules:
    try:
        imp.find_module(module)
        print("checking python module " + magenta(module) + " " + green("✔"))
    except ImportError:
        fatal(False, module, "pip3 install " + module)

# check git remote just in case somebody has the old one
result = run(['git', 'config', '--get', 'remote.origin.url'], stderr=PIPE, stdout=PIPE, universal_newlines=True)
if (result.returncode == 0):
    p = re.compile('(git@|https://)github.com(/|:)rIGS2016/')
    if (p.match(result.stdout)):
        print("Yo code poet, you have the " + bold("old remote repo. ") + red("✖"))
        print("You need to run this:")
        print()
        print(green(" git remote set-url origin git@github.com:rIGSteam/Potatobot.git"))
        print()
        exit(1)

print()
print(bold("Everything looks good, let's go write some robot code"))
print()

