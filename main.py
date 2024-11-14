from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Color, Axis, Direction, Button
from pybricks.tools import wait, Matrix, StopWatch, hub_menu
from pybricks.robotics import DriveBase
from pybricks.hubs import PrimeHub

# Constants
DRIVEBASE_WHEEL_DIAMETER = 88
DRIVEBASE_AXLE_TRACK = 115 # confirm this value
LOW_VOLTAGE = 7000
HIGH_VOLTAGE = 8000
MENU_OPTIONS = ["1", "2", "3", "4", "7", '8', "C"]
ROBOT_SPEED = 900
ROBOT_ACCELERATION = 900
ROBOT_TURN_RATE = 900
ROBOT_TURN_ACCELERATION = 900
ROBOT_MAX_TORQUE = 1000
ROBOT_DUTY_LIMIT = 50

# Variables
battery_status_light = Color.GREEN

# Define the Robot
class Robot:
    def __init__(self):
        # DRIVE MOTORS: Left () Right () Big () Small ()
        self.leftDrive = Motor(Port.F, Direction.COUNTERCLOCKWISE)
        self.rightDrive = Motor(Port.B)
        self.rightBig = Motor(Port.C)
        self.leftBig = Motor(Port.D)

        # Defines the drivebase
        self.driveBase = DriveBase(self.leftDrive, self.rightDrive, DRIVEBASE_WHEEL_DIAMETER, DRIVEBASE_AXLE_TRACK)
        self.driveBase.use_gyro(False)
        self.driveBase.settings(
            straight_speed=ROBOT_SPEED, 
            straight_acceleration=ROBOT_ACCELERATION, 
            turn_rate=ROBOT_TURN_RATE, 
            turn_acceleration=ROBOT_TURN_ACCELERATION
        )
        self.leftDrive.control.limits(ROBOT_SPEED, ROBOT_ACCELERATION, ROBOT_MAX_TORQUE)
        self.rightDrive.control.limits(ROBOT_SPEED, ROBOT_ACCELERATION, ROBOT_MAX_TORQUE)

        # Defines the hub
        self.hub = PrimeHub(front_side=-Axis.Y)
        self.hub.system.set_stop_button(Button.BLUETOOTH)
    
    def Battery(self, val:float):
        return val + (val*(100-Rescale(self.hub.battery.voltage(), LOW_VOLTAGE, HIGH_VOLTAGE, 1, 100)))
        
    # add wait parameter to plug in to functions for these below
    def MoveRightMotorInDegrees(self, degrees:float, speed:float=ROBOT_TURN_RATE, wait:bool = True):
        # degrees = Robot.Battery(degrees)
        # speed = Robot.Battery(speed)
        self.driveBase.use_gyro(True)
        self.rightBig.run_angle(speed, degrees, wait=wait)
        self.driveBase.use_gyro(False)
    
    def MoveLeftMotorInDegrees(self, degrees:float, speed:float=ROBOT_TURN_RATE, wait:bool = True):
        # degrees = Robot.Battery(degrees)
        # speed = Robot.Battery(speed)
        self.driveBase.use_gyro(True)
        self.leftBig.run_angle(speed, degrees, wait=wait)
        self.driveBase.use_gyro(False)
    
    def MoveRightMotorUntilStalled(self, speed:float=ROBOT_TURN_RATE, duty_limit:int=50):
        # speed = Robot.Battery(speed)
        self.rightBig.run_until_stalled(speed, duty_limit=duty_limit)

    def MoveLeftMotorUntilStalled(self, speed:float=ROBOT_TURN_RATE, duty_limit:int=20):
        # speed = Robot.Battery(speed)
        self.leftBig.run_until_stalled(speed, duty_limit=duty_limit)
    
    def DriveForDistance(self, distance:float, wait:bool = True, speed=ROBOT_SPEED):
        # speed = Robot.Battery(speed)
        # distance = Robot.Battery(distance)
        self.driveBase.use_gyro(True)
        self.driveBase.settings(straight_speed=speed)
        self.driveBase.straight(distance, wait=wait)
        self.driveBase.settings(straight_speed=ROBOT_SPEED)
        self.driveBase.use_gyro(False)
    
    def DriveForMilliseconds(self, milliseconds:float, speed:float=ROBOT_SPEED):
        # speed = Robot.Battery(speed)
        self.driveBase.drive(speed, 0)
        wait(milliseconds)
        self.driveBase.stop()
    
    def TurnInPlace(self, degrees:float, wait:bool=True):
        # degrees = Robot.Battery(degrees)
        self.driveBase.use_gyro(True)
        self.driveBase.turn(degrees, wait=wait)
        self.driveBase.use_gyro(False)
    
    def Curve(self, radius:float, angle:float, wait:bool=True):
        self.driveBase.use_gyro(True)
        self.driveBase.curve(radius, angle, wait=wait)
        self.driveBase.use_gyro(False)

    def DisplayNumber(self, number:int):
        self.hub.display.off()
        self.hub.display.number(number)

    def StatusLight(self, color:Color):
        self.hub.light.off()
        self.hub.light.on(color)
    
    def BatteryDisplay(self):
        # display battery of hub
        v = self.hub.battery.voltage()
        vPct = Rescale(v, LOW_VOLTAGE, HIGH_VOLTAGE, 1, 100)
        print(f"Battery %: {vPct}, Voltage: {v}")
        if vPct < 70:
            if vPct < 40:
                print("EMERGENCY: BATTERY LOW!")
                battery_status_light = Color.RED
            else:
                print("Battery is below 70% Please charge!")
                battery_status_light = Color.YELLOW
            self.StatusLight(battery_status_light)
        else:
            self.StatusLight(Color.GREEN)
    
    def CleanMotors(self):
        self.leftDrive.run_angle(999, 1000, wait=False)
        self.rightDrive.run_angle(999, 1000, wait=False)
        self.leftBig.run_angle(999, 1000, wait=False)
        self.rightBig.run_angle(999, 1000)

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

class Missions:
    # Sorted in order of what we are doing

    def ShippingLanes(r:Robot):
        pass
    
    def Seaweed(r:Robot):
        pass

    def Whales(r:Robot):
        pass

    def Octopus(r:Robot):
        pass

    def CrabBoxes(r:Robot):
        pass

    def CoralNursery(r:Robot):
        pass

    def Shark(r:Robot):
        pass

    def CoralReef(r:Robot):
        pass
    
    def ScubaDiver(r:Robot):
        pass
    
    def ResearchShip(r:Robot):
        pass

    def AnglerFish(r:Robot):
        pass

    def Submarine(r:Robot):
        pass 

# Runs
class Run:
    def One(r:Robot):
        # Away Location
        r.DriveForDistance(30)
        r.TurnInPlace(45)
        r.DriveForDistance(330)
        r.TurnInPlace(-33)
        r.DriveForDistance(300)
        r.TurnInPlace(40)
        r.DriveForDistance(250)
        r.TurnInPlace(40)
        r.DriveForDistance(1100)
        r.DriveForDistance(-100)
        r.TurnInPlace(45)
        r.DriveForDistance(1000)
        # Home Location

    def Two(r:Robot):
        # Home Location
        r.DriveForDistance(50)
        r.TurnInPlace(-45)
        r.DriveForDistance(600)
        r.DriveForDistance(-150)
        r.TurnInPlace(40)
        r.DriveForDistance(430)
        r.TurnInPlace(125)
        r.MoveLeftMotorUntilStalled(-500)
        r.DriveForDistance(120)
        r.MoveLeftMotorInDegrees(90, 900)
        r.TurnInPlace(45)
        r.DriveForDistance(700)
        # Home Location
        
    def Three(r:Robot):
        pass

def Run4(r:Robot):
    # Away Location
    r.TurnInPlace(30)
    r.DriveForDistance(490)
    r.TurnInPlace(60)
    r.DriveForDistance(200)
    wait(500)
    r.DriveForDistance(-200)
    r.DriveForDistance(60)
    r.TurnInPlace(-50)
    r.DriveForDistance(-1000)
    # Away Location

def Run5(r:Robot):
    # Away Location
    pass
    # Away Location

def Run6(r:Robot):
    # Away Location
    pass
    # End

def Run7(r:Robot):
    pass

def Run8(r:Robot):
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
    start_time = stopwatch.time()
    if selected == "1":
        Run.One(r)
        all_start_time = stopwatch.time()
    elif selected == "2":
        Run.Two(r)
    elif selected == "3":
        Run.Three(r)
    elif selected == "4":
        Run.Four(r)
    elif selected == "5":
        Run.Five(r)
    elif selected == "6":
        Run.Six(r)
    elif selected == "7":
        Run.Seven(r)
    elif selected == '8':
        Run.Eight(r)
        print("All missions complete.\n---------------------------------------\nRESULTS:")
        try:
            alltotaltime = round((stopwatch.time() - all_start_time)/ 1000, 1)
            print(f"Total time: {alltotaltime} seconds. This is {round(alltotaltime/150*100, 1)}% of the time")
            if alltotaltime > 150:
                print(f"Time exceeded by {150-alltotaltime} seconds.")
            print("---------------------------------------")
        except:
            print("You didn't run everything.")
    print(f"Done running #{selected}. Time: {round((stopwatch.time() - start_time)/ 1000, 1)} seconds.")
    r.StatusLight(battery_status_light)
    return selected

# create robot
my_robot = Robot()

# create stopwatch
stopwatch = StopWatch()

# display battery
my_robot.BatteryDisplay()

# run menu
last_run = "C"
while True:
    # Test this later
    current_menu = []
    for i in range(len(MENU_OPTIONS)):
        current_menu.append(MENU_OPTIONS[(i+MENU_OPTIONS.index(last_run)+1) % len(MENU_OPTIONS)])
    selected = hub_menu(*current_menu)
    if selected != "C":
        last_run = RunMission(my_robot, selected)
    else:
        if selected == 'C':
            my_robot.CleanMotors()