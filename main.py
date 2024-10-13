from pybricks.pupdevices import Motor, Button
from pybricks.parameters import Port, Color, Icon
from pybricks.tools import wait, Matrix, StopWatch, hub_menu
from pybricks.robotics import DriveBase
from pybricks.hubs import PrimeHub

# Constants
DRIVEBASE_WHEEL_DIAMETER = 56
DRIVEBASE_AXLE_TRACK = 105 # confirm this value
LOW_VOLTAGE = 7000
HIGH_VOLTAGE = 8000
MENU_OPTIONS = ["1", "2", "3", "4", "5", "6", "7", "C"]

# Define the Robot
class Robot:
    def __init__(self):
        # DRIVE MOTORS: Left (A) Right (B) Big (E) Small (F)
        self.leftDrive = Motor(Port.A)
        self.rightDrive = Motor(Port.B)
        self.big = Motor(Port.E)
        self.small = Motor(Port.F)

        # Defines the drivebase
        self.driveBase = DriveBase(self.leftDrive, self.rightDrive, DRIVEBASE_WHEEL_DIAMETER, DRIVEBASE_AXLE_TRACK)
        self.driveBase.use_gyro(True)

        # Defines the hub
        self.hub = PrimeHub()
    
    # add wait parameter to plug in to functions for these below
    def MoveSmallMotorInDegrees(self, degrees:int, speed:int=100, wait:bool = True):
        self.small.run_angle(speed, degrees, wait=wait)
    
    def MoveBigMotorInDegrees(self, degrees:int, speed:int=100, wait:bool = True):
        self.big.run_angle(speed, degrees, wait=wait)
    
    def DriveForDistance(self, distance:int, wait:bool = True):
        self.driveBase.straight(distance, wait=wait)
    
    def DriveForMilliseconds(self, milliseconds:int, speed:int=100):
        self.driveBase.drive(speed, 0)
        wait(milliseconds)
        self.driveBase.stop()
    
    def TurnInPlace(self, degrees:int, wait:bool=True):
        self.driveBase.turn(degrees, wait=wait)
    
    def Curve(self, radius:int, angle:int, wait:bool=True):
        self.driveBase.curve(radius, angle, wait=wait)

    def DisplayNumber(self, number:int):
        self.hub.display.off()
        self.hub.display.number(number)

    def StatusLight(self, color:Color):
        self.hub.light.off()
        self.hub.light.on(color)
    
    def BatteryDisplay(self):
        # display battery of hub
        v = 7900
        vPct = Rescale(v, LOW_VOLTAGE, HIGH_VOLTAGE)
        print(f"Battery %: {vPct}")
        if vPct < 70:
            print("Battery is below 70% Please charge!")
            self.StatusLight(Color.RED)
        else:
            self.StatusLight(Color.GREEN)
    
    def CleanMotors(self):
        self.leftDrive.run_angle(200, 1000, wait=False)
        self.rightDrive.run_angle(200, 1000, wait=False)
        self.big.run_angle(200, 1000, wait=False)
        self.small.run_angle(200, 1000)

class Animations:
    running = [
        Matrix([
            [0, 0, 100, 100, 100],
            [100, 0, 0, 0, 100],
            [100, 0, 0, 0, 100],
            [100, 0, 0, 0, 100],
            [100, 100, 100, 0, 0]
        ]), Matrix([
            [100, 0, 0, 100, 100],
            [100, 0, 0, 0, 100],
            [100, 0, 0, 0, 100],
            [100, 0, 0, 0, 100],
            [100, 100, 0, 0, 100]
        ]), Matrix([
            [100, 100, 0, 0, 100],
            [100, 0, 0, 0, 100],
            [100, 0, 0, 0, 100],
            [100, 0, 0, 0, 100],
            [100, 0, 0, 100, 100]
        ]), Matrix([
            [100, 100, 100, 0, 0],
            [100, 0, 0, 0, 100],
            [100, 0, 0, 0, 100],
            [100, 0, 0, 0, 100],
            [0, 0, 100, 100, 100]
        ]), Matrix([
            [100, 100, 100, 100, 0],
            [100, 0, 0, 0, 0],
            [100, 0, 0, 0, 100],
            [0, 0, 0, 0, 100],
            [0, 100, 100, 100, 100]
        ]), Matrix([
            [100, 100, 100, 100, 100],
            [100, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 100],
            [100, 100, 100, 100, 100]
        ]), Matrix([
            [100, 100, 100, 100, 100],
            [0, 0, 0, 0, 100],
            [0, 0, 0, 0, 0],
            [100, 0, 0, 0, 0],
            [100, 100, 100, 100, 100]
        ]), Matrix([
            [0, 100, 100, 100, 100],
            [0, 0, 0, 0, 100],
            [100, 0, 0, 0, 100],
            [100, 0, 0, 0, 0],
            [100, 100, 100, 100, 0]
        ])
    ]

# run functions
def Run1(r:Robot):
    r.TurnInPlace(-90)
    r.DriveForDistance(100)
    # do 4 square crab thing
    r.DriveForDistance(-20)
    r.TurnInPlace(90)
    r.DriveForDistance(100)
    r.TurnInPlace(-45)
    # do octopus push thing
    r.DriveForDistance(30)
    r.DriveForDistance(-30)
    r.TurnInPlace(90)
    r.DriveForDistance(100)
    # do leafy green thing

def Run2(r:Robot):
    pass

def Run3(r:Robot):
    pass

def Run4(r:Robot):
    pass

def Run5(r:Robot):
    pass

def Run6(r:Robot):
    pass

def Run7(r:Robot):
    pass

# Utility functions
def Rescale(value, in_min, in_max, out_min, out_max):
    neg = value / abs(value) # will either be 1 or -1
    value = abs(value)
    if value < in_min: value = in_min
    if value > in_max: value = in_max
    retvalue = (value - in_min) * (out_max / (in_max - in_min))
    if retvalue > out_max: retvalue = out_max
    if retvalue < out_min: retvalue = out_min
    return retvalue * neg

def RunMission(r:Robot, selected):
    # run current selection
    r.StatusLight(Color.YELLOW)
    r.hub.display.animate(Animations.running, 30)
    print(f"Running #{selected}...")
    start_time = StopWatch.time()
    eval(f'Run{str(selected)}(r)')
    print(f"Done running #{selected}. Time: {StopWatch.time() - start_time}")
    r.StatusLight(Color.GREEN)
    return selected

# create robot
my_robot = Robot()

# display battery
my_robot.BatteryDisplay()

# run menu
last_run = "C"
while True:
    # Test this later
    current_menu = []
    for i in range(len(MENU_OPTIONS)):
        current_menu.append(MENU_OPTIONS[(i+MENU_OPTIONS.index(last_run)+1) % len(MENU_OPTIONS)])
    selected = hub_menu(current_menu)
    if not selected == "C":
        last_run = RunMission(my_robot, selected)
    else:
        my_robot.CleanMotors()