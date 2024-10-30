from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Color, Axis, Direction, Button
from pybricks.tools import wait, Matrix, StopWatch, hub_menu
from pybricks.robotics import DriveBase
from pybricks.hubs import PrimeHub

# Constants
DRIVEBASE_WHEEL_DIAMETER = 56
DRIVEBASE_AXLE_TRACK = 105 # confirm this value
LOW_VOLTAGE = 7000
HIGH_VOLTAGE = 8000
MENU_OPTIONS = ["1", "2", "3", "4", "5", "6", "7", '8', "C"]
ROBOT_SPEED = 500
ROBOT_ACCELERATION = 500
ROBOT_TURN_RATE = 500
ROBOT_TURN_ACCELERATION = 500
ROBOT_MAX_TORQUE = 1000
ROBOT_DUTY_LIMIT = 50

# Variables
battery_status_light = Color.GREEN

# Define the Robot
class Robot:
    def __init__(self):
        # DRIVE MOTORS: Left (A ) Right (B) Big (E) Small (F)
        self.leftDrive = Motor(Port.A, Direction.COUNTERCLOCKWISE)
        self.rightDrive = Motor(Port.B)
        self.big = Motor(Port.E)
        self.small = Motor(Port.F)

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
    
    # add wait parameter to plug in to functions for these below
    def MoveSmallMotorInDegrees(self, degrees:float, speed:float=ROBOT_TURN_RATE, wait:bool = True):
        self.driveBase.use_gyro(True)
        self.small.run_angle(speed, degrees, wait=wait)
        self.driveBase.use_gyro(False)
    
    def MoveBigMotorInDegrees(self, degrees:float, speed:float=ROBOT_TURN_RATE, wait:bool = True):
        self.driveBase.use_gyro(True)
        self.big.run_angle(speed, degrees, wait=wait)
        self.driveBase.use_gyro(False)
    
    def MoveSmallMotorUntilStalled(self, speed:float=ROBOT_TURN_RATE, duty_limit:int=ROBOT_DUTY_LIMIT):
        self.small.run_until_stalled(speed, duty_limit=duty_limit)

    def MoveBigMotorUntilStalled(self, speed:float=ROBOT_TURN_RATE, duty_limit:int=ROBOT_DUTY_LIMIT):
        self.big.run_until_stalled(speed, duty_limit=duty_limit)
    
    def DriveForDistance(self, distance:float, wait:bool = True):
        self.driveBase.use_gyro(True)
        self.driveBase.straight(distance, wait=wait)
        self.driveBase.use_gyro(False)
    
    def DriveForMilliseconds(self, milliseconds:float, speed:float=ROBOT_SPEED):
        self.driveBase.drive(speed, 0)
        wait(milliseconds)
        self.driveBase.stop()
    
    def TurnInPlace(self, degrees:float, wait:bool=True):
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
        self.big.run_angle(999, 1000, wait=False)
        self.small.run_angle(999, 1000)

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

    def ShippingLanes(r:Robot): # Start with the robot facing the boat in the middle about 7 cm away
        # Reset the angle
        r.MoveSmallMotorUntilStalled(500)
        r.MoveSmallMotorInDegrees(-75, 500)
        r.DriveForDistance(85)
        r.MoveSmallMotorInDegrees(-180, 500)
    
    def Seaweed(r:Robot):
        r.MoveBigMotorInDegrees(45)

    def Whales(r:Robot, whaleNum):
        if whaleNum == 1:
            #first whale
            r.MoveSmallMotorUntilStalled(500)
            r.DriveForDistance(-150)
            r.MoveSmallMotorInDegrees(-90)
        elif whaleNum == 2:
            #second whale not finished
            pass
        else:
            print("whaleNum is invalid [Missions.Whales]")

    def Octopus(r:Robot): # start with the robot facing the pusher in the middle
        r.DriveForDistance(-500)
        wait(100)
        r.DriveForDistance(500)

    def CrabBoxes(r:Robot):
        r.DriveForDistance(300, wait=False)
        r.MoveSmallMotorUntilStalled(500)
        r.MoveSmallMotorInDegrees(-65)
        r.DriveForDistance(300)
        r.TurnInPlace(90)
        r.DriveForDistance(380)
        r.TurnInPlace(-135)
        r.DriveForDistance(230)
        r.MoveSmallMotorUntilStalled(-500, 200)
        r.DriveForDistance(-150, 700)
        r.MoveSmallMotorUntilStalled(500)
        r.MoveSmallMotorInDegrees(-65)
        r.TurnInPlace(90)
        r.TurnInPlace(45)
        r.DriveForDistance(700)
        

    def CoralNursery(r:Robot):
        r.MoveBigMotorInDegrees(90)
        r.DriveForDistance(-100)
        r.TurnInPlace(-8)
        r.DriveForDistance(100)
        r.MoveSmallMotorInDegrees(720)
        
    def Shark(r:Robot):
        r.MoveSmallMotorInDegrees(-720)


    def CoralReef(r:Robot):
        r.MoveSmallMotorInDegrees(-720)
    
    def ScubaDiver(r:Robot):
        pass
    
    def ResearchShip(r:Robot, part):
        if part == 1:
            pass
        elif part == 2:
            pass
        else:
            print("Part is invalid [Missions.ResearchShip]")
        # add putting the things into the research ship here

    def AnglerFish(r:Robot):
        r.DriveForDistance(400)

    def Submarine(r:Robot):
        pass

# run functions
def Run1(r:Robot):
    # Home location
    r.DriveForDistance(345)
    r.TurnInPlace(43)
    # Boat mission
    Missions.ShippingLanes(r)
    r.DriveForDistance(-50)
    r.MoveSmallMotorInDegrees(90, 500)
    r.TurnInPlace(-45)
    r.DriveForDistance(300)
    r.TurnInPlace(-95)
    r.DriveForDistance(-65)
    # Seaweed mission
    Missions.Seaweed(r)
    r.DriveForDistance(50)
    r.TurnInPlace(-90)
    r.DriveForDistance(700)
    # Home location

def Run2(r:Robot):
    # Home location
    r.TurnInPlace(-45)
    r.DriveForDistance(130) 
    r.TurnInPlace(45)
    r.MoveSmallMotorUntilStalled(500)
    r.MoveSmallMotorInDegrees(-90, 500)
    r.DriveForDistance(970)
    r.DriveForDistance(-50)
    # Whales mission
    Missions.Whales(r, 1)
    r.DriveForDistance(-700)
    r.TurnInPlace(-90)
    r.DriveForDistance(-200)
    # Home location
    
def Run3(r:Robot):
    Missions.Octopus(r)

def Run4(r:Robot):
    # Home location
    r.TurnInPlace(-55)
    r.DriveForDistance(700)
    # Anglerfish Mission
    Missions.AnglerFish(r)
    r.TurnInPlace(-35)
    r.DriveForDistance(-200)
    # Octopus in the circle
    r.MoveBigMotorInDegrees(-180)
    # Sample to Away location
    r.DriveForDistance(50)
    r.TurnInPlace(15)
    r.DriveForDistance(300)
    r.TurnInPlace(-55)
    r.DriveForDistance(800)
    r.TurnInPlace(-45)
    r.DriveForDistance(200)
    # Away Location

def Run5(r:Robot):
    # Away Location
    r.TurnInPlace(45)
    print('turn')
    r.DriveForDistance(100)
    print('drive')
    r.TurnInPlace(-45)
    print('turn')
    r.MoveSmallMotorUntilStalled(-500, 30)
    r.MoveBigMotorUntilStalled(-500)
    r.DriveForDistance(400)
    # Coral Nursery Mission
    Missions.CoralNursery(r)
    r.TurnInPlace(15+90)
    r.DriveForDistance(100)
    r.TurnInPlace(-90)
    r.DriveForDistance(200)
    r.TurnInPlace(-45)
    r.DriveForDistance(50)
    # Shark Mission
    Missions.Shark(r)
    # Knock over the sample
    r.DriveForDistance(-200)
    r.DriveForDistance(100)
    r.TurnInPlace(45)
    r.DriveForDistance(150)
    r.MoveSmallMotorUntilStalled(500)
    r.TurnInPlace(45)
    r.DriveForDistance(100)
    # Coral Reef Mission
    Missions.CoralReef(r)
    r.DriveForDistance(-50)
    r.TurnInPlace(-45)
    r.DriveForDistance(-400)
    # Away Location

def Run6(r:Robot):
    # Away Location
    # Put the coral onto the coral nursery
    r.DriveForDistance(600)
    wait(500)
    r.DriveForDistance(-600)
    # Away Location

def Run7(r:Robot):
    # Away Location
    # Research Ship Mission (Using arm to pull)
    Missions.ResearchShip(r, 1)
    
    # Crab Boxes Mission
    Missions.CrabBoxes(r)
    
    # Using back to push
    Missions.ResearchShip(r, 2)
    
    # Home Location

def Run8(r:Robot):
    # Home Location

    # Angler Fish Mission
    Missions.AnglerFish(r)

    # Submarine Mission
    Missions.Submarine(r)

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
        Run1(r)
        all_start_time = stopwatch.time()
    elif selected == "2":
        Run2(r)
    elif selected == "3":
        Run3(r)
    elif selected == "4":
        Run4(r)
    elif selected == "5":
        Run5(r)
    elif selected == "6":
        Run6(r)
    elif selected == "7":
        Run7(r)
    elif selected == '8':
        Run8(r)
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
    if not selected == "C":
        last_run = RunMission(my_robot, selected)
    else:
        my_robot.CleanMotors()