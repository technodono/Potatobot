import wpilib, math

MOTOR1_PWM=0                                                        #assigns the motors to pwm ports
MOTOR2_PWM=1
MOTOR3_PWM=2
MOTOR4_PWM=3
PORT1=1
PORT2=5
PORT3=0

class MyRobot(wpilib.IterativeRobot):
    def robotInit(self):                                            #creates all the objects needed to operate the robot
        self.pdp = wpilib.PowerDistributionPanel()
        self.motor1 = wpilib.VictorSP (MOTOR1_PWM)
        self.motor2 = wpilib.VictorSP (MOTOR2_PWM)
        self.motor3 = wpilib.VictorSP(MOTOR3_PWM)
        self.motor4 = wpilib.VictorSP(MOTOR4_PWM)
        self.stick = wpilib.Joystick(PORT3)
        self.multiplier = 1                                         #creates a multiplayer to adjust the speed
        self.throttle_toggle = False
        self.timer = wpilib.Timer()                                 #creates a timer to time the autonomous mode

    def disabledInit(self):
        self.logger.info("Disabled Mode")

    def testInit(self):
        self.logger.info("Test Mode")

    #The following lines define the arcade drive settings
    def arcade_drive(self, forward, turn):
        left_value = -forward+turn
        left_value *= math.fabs(left_value)
        left_value *= self.multiplier
        right_value = -forward-turn
        right_value *= math.fabs(right_value)
        right_value *= self.multiplier
        self.motor1.set(left_value)
        self.motor2.set(left_value)
        self.motor3.set(-right_value)
        self.motor4.set(-right_value)

    def autonomousInit(self):                                       #resets and starts the timer at the beginning of autonomous
        self.logger.info("Autonomous Mode")
        self.timer.reset()
        self.timer.start()

#The following lines tell the robot what to do in autonomous
    def autonomousPeriodic(self):
        if self.timer.get()>2:
            self.arcade_drive(0,0)                                  #this sets up code that makes the robot drive forward for two seconds, hence the timer
        else:
            self.arcade_drive(0.7,0)                                #sets the robot to drive forward at 0.7 of the normal speed

    def teleopInit(self):
        self.logger.info("Teleoperated Mode")

#The following lines tell the robot what to do in teleop
    def teleopPeriodic(self):
        self.arcade_drive(-self.stick.getY(), -self.stick.getZ())   #Controls the Joystick, forwards, backwards,turn
        if self.stick.getRawButton(5):                              #assigns button 5 to multiply joystick position to 2, making it accelerate faster
            self.multiplier=2
            self.throttle_toggle = False
        if self.stick.getRawButton(2):                              #assigns button 2 to multiply joystick position by 1 (normal speed)
            self.multiplier=1
            self.throttle_toggle = False
        if self.stick.getRawButton(3):                              #assigns button 3 to 0.35 of 1, making the robot slower
            self.multiplier=0.35
            self.throttle_toggle = False
        if self.stick.getRawButton(4):                              #assigns button 4 to iuse the throttle to adjust speed.
            self.throttle_toggle = True
        if self.throttle_toggle:
            self.multiplier = (-self.stick.getThrottle()+1)/2

#These lines are needed to turn the motors off when the robot is disabled
    def disabledPeriodic(self):
        self.motor1.set(0)
        self.motor2.set(0)
        self.motor3.set(0)
        self.motor4.set(0)

#The following lines of code are ALWAYS needed to deploy code onto the robot
if __name__ == '__main__':
    wpilib.run(MyRobot)

#By Alex Rowell, Ben Briganti, Lucca Buonamano and Lex Martin