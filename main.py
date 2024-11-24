from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Color, Axis, Direction, Button, Stop
from pybricks.tools import wait as sleep, Matrix, StopWatch, hub_menu
from pybricks.robotics import DriveBase
from pybricks.hubs import PrimeHub

# Constants
DRIVEBASE_WHEEL_DIAMETER = 88 # 56 is small, 88 is big
DRIVEBASE_AXLE_TRACK = 115 # confirm this value
LOW_VOLTAGE = 7000
HIGH_VOLTAGE = 8300
MENU_OPTIONS = ["1", "2", "3", "4", "5", "6", "7", '8', "C"]
ROBOT_SPEED = 500
ROBOT_ACCELERATION = 750
ROBOT_TURN_RATE = 750
ROBOT_TURN_ACCELERATION = 3000
ROBOT_MAX_TORQUE = 1000

# Variables
battery_status_light = Color.GREEN
turn_ratio = {
    "1": 1.02,
    "2": 1,
    "3": 1.165,
    "4": 1.05942,
    "5": 1,
    "6": 1,
    "7": 1,
    "8": 1.165
}

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
    
    def Battery(self, val:float): # Not used
        return val + (val*(100-Rescale(self.hub.battery.voltage(), LOW_VOLTAGE, HIGH_VOLTAGE, 1, 100)))
        
    def MoveRightMotorInDegrees(self, degrees, speed=ROBOT_TURN_RATE, then=Stop.BRAKE, wait=True):
        # degrees = Robot.Battery(degrees)
        # speed = Robot.Battery(speed)
        self.rightBig.run_angle(speed, degrees, then, wait)
    
    def MoveLeftMotorInDegrees(self, degrees, speed=ROBOT_TURN_RATE, then=Stop.BRAKE, wait=True):
        # degrees = Robot.Battery(degrees)
        # speed = Robot.Battery(speed)
        self.leftBig.run_angle(speed, degrees, then, wait)
    
    def MoveRightMotorUntilStalled(self, speed=ROBOT_TURN_RATE, then=Stop.COAST, duty_limit=50):
        # speed = Robot.Battery(speed)
        self.rightBig.run_until_stalled(speed, then, duty_limit)

    def MoveLeftMotorUntilStalled(self, speed=ROBOT_TURN_RATE, then=Stop.COAST, duty_limit=20):
        # speed = Robot.Battery(speed)
        self.leftBig.run_until_stalled(speed, then, duty_limit)
    
    def DriveForDistance(self, distance, then=Stop.BRAKE, wait=True, speed=ROBOT_SPEED):
        # speed = Robot.Battery(speed)
        # distance = Robot.Battery(distance)
        self.driveBase.settings(straight_speed=speed)
        self.driveBase.straight(distance, then, wait)
        self.driveBase.settings(straight_speed=ROBOT_SPEED)
    
    def DriveForMilliseconds(self, milliseconds, speed=ROBOT_SPEED):
        # speed = Robot.Battery(speed)
        self.driveBase.drive(speed, 0)
        sleep(milliseconds)
        self.driveBase.brake()
    
    def TurnInPlace(self, degrees, then=Stop.BRAKE, wait=True, use_gyro=True):
        global selected
        if use_gyro:
            self.driveBase.use_gyro(True)
        self.driveBase.turn(degrees*turn_ratio[selected], then, wait)
        self.driveBase.use_gyro(False)
    
    def Curve(self, radius, angle, then=Stop.BRAKE, wait=True):
        self.driveBase.use_gyro(True)
        self.driveBase.curve(radius, angle, then, wait)
        self.driveBase.use_gyro(False)

    def StatusLight(self, color):
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
    """
    Game missions
    1. Coral Nursery
        A. Hang Coral
        B. 
    2. Shark
        A. Pickup Shark
        B. Put Shark into the habitat
    3. Coral Reef
        A. Flip up the  coral
    4. Scuba Diver
        A. Pick up diver
        B. Put diver onto coral reef
    5. Anglerfish
        A. Flick angler fish into the ship
    6. Raise the mast
    7. Kraken's treasure
    8. Artificial habtat
    9. Unexpected encounter
    10. Send over the submersible
    11. Sonar Discovery
    12. Feed the whale
    13. Change shipping lanes
    14. Sample colletion
        A. Kelp
        B. Seabed
        C. Water
        D. Treasure Chest
        E. Trident Parts
    15. Research Vessel
    """
    # Mission 1: Coral Nursery
    class CoralNursery:
        def Hang(r:Robot):
            pass
        
        def Buds(r:Robot):
            pass
    # Mission 2: Shark
    class Shark:
        def Pickup(r:Robot):
            pass
        
        def Deliver(r:Robot):
            pass
        
    # Mission 3: Coral Reef
    def CoralReef(r:Robot):
        pass
    
    # Mission 4: Scuba Diver
    class ScubaDiver:
        def Pickup(r:Robot):
            pass
        
        def Delivery(r:Robot):
            pass
        
    # Mission 5: Angler Fish
    def AnglerFish(r:Robot):
        pass
    
    # Mission 6: Raise the Mast
    def RaiseMast(r:Robot):
        pass
    
    # Mission 7: Kraken's Treasure
    def Treasure(r:Robot):
        pass
    
    # Mission 8: Artificial Habitat
    class ArtificialHabitat:
        def Part1(r:Robot):
            pass
        
        def Part2(r:Robot):
            pass
    
    # Mission 9: Unexpected Encounter
    def Octopus(r:Robot):
        pass
    
    # Mission 10: Send Over the Submersible
    def Submersible(r:Robot):
        pass
    
    # Mission 11: Sonar Discovery
    class SonarDiscovery:
        def Whale1(r:Robot):
            pass
        
        def Whale2(r:Robot):
            pass
        
    # Mission 12: Feed the Whale
    def FeedWhale(r:Robot):
        pass
    
    # Mission 13: Change Shipping Lanes
    def ShippingLanes(r:Robot):
        pass
    
    # Mission 14: Sample Collection
    class Samples:
        def Seabed(r:Robot):
            r.MoveLeftMotorInDegrees(-700)
            r.DriveForDistance(60)
            r.MoveLeftMotorInDegrees(700, wait=False)
        
        def Kelp(r:Robot):
            r.TurnInPlace(35)
            r.DriveForDistance(50)
        
        def Water(r:Robot):
            pass
        
        def Trident(r:Robot):
            pass
        
        def Delivery(r:Robot):
            pass
        
    # Mission 15: Research Vessel
    def ResearchVessel(r:Robot):
        pass

# Runs
class Run:
    def One(r:Robot):
        # Away Location
        r.DriveForDistance(30)
        r.TurnInPlace(60)
        r.DriveForDistance(285)
        r.TurnInPlace(-60)
        r.DriveForDistance(380)
        r.TurnInPlace(57)
        r.DriveForDistance(290-15)
        r.TurnInPlace(33)
        r.DriveForDistance(235)
        Missions.Samples.Seabed(r)
        r.TurnInPlace(45)
        sleep(1000)
        r.DriveForDistance(100)
        r.TurnInPlace(-45)
        r.DriveForDistance(550)
        Missions.Samples.Kelp(r)
        r.DriveForDistance(-75)
        r.TurnInPlace(-10)
        r.DriveForDistance(-180)
        r.TurnInPlace(45)
        r.DriveForDistance(1000)
        # Home Location
 
    def Two(r:Robot):
        # Home Location
        r.DriveForDistance(295)
        r.TurnInPlace(-49)
        r.MoveRightMotorUntilStalled(-500, duty_limit=20)
        r.MoveRightMotorInDegrees(20)
        r.DriveForDistance(70)
        r.TurnInPlace(30)
        r.MoveRightMotorInDegrees(360)
        r.MoveRightMotorInDegrees(100)
        r.MoveRightMotorInDegrees(140, wait=False)
        r.DriveForDistance(-40)
        sleep(1000)
        r.MoveRightMotorInDegrees(-90, wait=False)
        r.DriveForDistance(30)
        r.DriveForDistance(100)
        r.DriveForDistance(50)
        r.DriveForDistance(365)
        r.MoveLeftMotorInDegrees(360*2)
        r.DriveForDistance(-40)
        r.DriveForDistance(-350)
        r.TurnInPlace(-70)
        r.DriveForDistance(450, speed=1500)
        r.MoveRightMotorUntilStalled(-500, duty_limit=20)
        r.DriveForDistance(-600)
        # Home Location
        
    def Three(r:Robot):
        r.DriveForDistance(300)
        r.hub.imu.reset_heading(0)
        r.TurnInPlace(-90)
        print("Heading: " + str(r.hub.imu.heading()))
        for _ in range(3):
            r.TurnInPlace(-90-r.hub.imu.heading())
        print("Fixed: " + str(r.hub.imu.heading()))
        r.hub.imu.reset_heading(0)
        r.DriveForDistance(565)
        r.TurnInPlace(45)
        print("Heading: " + str(r.hub.imu.heading()))
        for _ in range(3):
            r.TurnInPlace(45-r.hub.imu.heading())
        print("Fixed: " + str(r.hub.imu.heading()))
        r.DriveForDistance(600)
        r.DriveForDistance(-400)
        r.TurnInPlace(30)
        r.DriveForDistance(450)
        r.DriveForDistance(-150z)
        r.TurnInPlace(-75)
        r.DriveForDistance(150)
        r.MoveLeftMotorInDegrees(180)
        r.DriveForDistance(600)
        r.TurnInPlace(-90)
        r.DriveForDistance(600)

    def Four(r:Robot):
        # Away Location
        r.TurnInPlace(30)
        r.DriveForDistance(490)
        r.TurnInPlace(60)
        r.DriveForDistance(200)
        sleep(500)
        r.DriveForDistance(-200)
        r.DriveForDistance(60)
        r.TurnInPlace(-50)
        r.DriveForDistance(-1000)
        # Away Location

    def Five(r:Robot):
        r.MoveRightMotorInDegrees(360)

    def Six(r:Robot):
        r.DriveForDistance(400)
        r.DriveForDistance(-400)

    def Seven(r:Robot):
        while True:
            pass
            if 0 != 0:
                break

    def Eight(r:Robot):
        r.TurnInPlace(90)

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
        print("All missions complete.\n---------------------------------------\nRESULTS:")
        try:
            alltotaltime = round((stopwatch.time() - all_start_time)/ 1000, 1)
            print(f"Total time: {alltotaltime} seconds. This is {round(alltotaltime/150*100, 1)}% of the time")
            if alltotaltime > 150:
                print(f"Time exceeded by {150-alltotaltime} seconds.")
            print("---------------------------------------")
        except:
            print("You didn't run everything.")
    elif selected == "7":
        Run.Seven(r)
    elif selected == '8':
        Run.Eight(r)
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