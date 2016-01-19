import wpilib, math

MOTOR1_PWM=0
MOTOR2_PWM=1
MOTOR3_PWM=2
MOTOR4_PWM=3
PORT1=1
PORT2=5
PORT3=0

class MyRobot(wpilib.IterativeRobot):
    def robotInit(self):
        self.pdp = wpilib.PowerDistributionPanel()
        self.motor1 = wpilib.VictorSP (MOTOR1_PWM)
        self.motor2 = wpilib.VictorSP (MOTOR2_PWM)
        self.motor3 = wpilib.VictorSP(MOTOR3_PWM)
        self.motor4 = wpilib.VictorSP(MOTOR4_PWM)
        self.stick = wpilib.Joystick(PORT3)
        self.multiplier = 1
        self.throttle_toggle = False
        self.timer = wpilib.Timer()


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

    def autonomousInit(self):
        self.timer.reset()
        self.timer.start()

    def autonomousPeriodic(self):
        if self.timer.get()>2:
            self.arcade_drive(0,0)
        else:
            self.arcade_drive(0.7,0)

    def teleopPeriodic(self):
        self.arcade_drive(-self.stick.getY(), -self.stick.getZ())
        if self.stick.getRawButton(5):
            self.multiplier=2
            self.throttle_toggle = False
        if self.stick.getRawButton(2):
            self.multiplier=1
            self.throttle_toggle = False
        if self.stick.getRawButton(3):
            self.multiplier=0.35
            self.throttle_toggle = False
        if self.stick.getRawButton(4):
            self.throttle_toggle = True
        if self.throttle_toggle:
            self.multiplier = (-self.stick.getThrottle()+1)/2

    def disabledPeriodic(self):
        self.motor1.set(0)
        self.motor2.set(0)
        self.motor3.set(0)
        self.motor4.set(0)

if __name__ == '__main__':
    wpilib.run(MyRobot)