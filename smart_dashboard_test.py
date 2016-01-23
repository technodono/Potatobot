import wpilib

class Smart_Dashboard_Test:
    def __init__(self):
        self.words = [[None,0],['This',0.2],['is',0.4],['major',0.5],['Tom',0.5],['to',0.3],['ground',0.5],['control,',0.5],['',1],['I\'m',0.3],['stepping',0.7],['through',0.4],['the',0.3],['door',1],['',1.5],['and',0.3],['I\'m',0.3],['floating',0.7],['in',0.4],['a',0.4],['most',0.4],['peculiar',0.9],['way',0.5],['',1.8],['and',0.4],['the',0.4],['stars',0.4],['look',0.4],['very',0.6],['different',1],['today',1.5],['',2.2],['here',2.2],['am',0.4],['I',0.4],['floating',0.4],['round',0.2],['my',0.2],['tincan',0.7],['',100]]
        self.stage = 1
        self.end = 23
        self.start = None

    def smart_dashboard_test(self,timer):
        time = timer.get()
        if self.stage == 1:
            wpilib.SmartDashboard.putString('word', self.words[1][0])
            self.start = time + self.words[1][1]
            self.stage = 2
        elif time > self.start:
            wpilib.SmartDashboard.putString('word', self.words[self.stage][0])
            self.start = time + self.words[self.stage][1]
            self.stage += 1