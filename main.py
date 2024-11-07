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
MENU_OPTIONS = ["1", "2", "3", "4", '5', '6', "7", '8', "C"] 
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
        # DRIVE MOTORS: LeftDrive (F) RightDrive (B) right (D) left (C)
        self.leftDrive = Motor(Port.F, Direction.COUNTERCLOCKWISE)
        self.rightDrive = Motor(Port.B)
        self.right = Motor(Port.D)
        self.left = Motor(Port.C)

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
    def MoveSmallMotorInDegrees(self, degrees:float, speed:float=ROBOT_TURN_RATE, wait:bool = True):
        self.left.run_angle(speed, degrees, wait=wait)
    
    def MoveBigMotorInDegrees(self, degrees:float, speed:float=ROBOT_TURN_RATE, wait:bool = True):
        self.right.run_angle(speed, degrees, wait=wait)
    
    def MoveSmallMotorUntilStalled(self, speed:float=ROBOT_TURN_RATE, duty_limit:int=50):
        self.left.run_until_stalled(speed, duty_limit=duty_limit)

    def MoveBigMotorUntilStalled(self, speed:float=ROBOT_TURN_RATE, duty_limit:int=20):
        self.right.run_until_stalled(speed, duty_limit=duty_limit)
    
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
        self.right.run_angle(999, 1000, wait=False)
        self.left.run_angle(999, 1000)

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
            pass
        
        def Kelp(r:Robot):
            pass
        
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
        # Home location
        r.DriveForDistance(345)
        r.TurnInPlace(43)
        # Boat mission
        Missions.ShippingLanes(r)
        r.DriveForDistance(-50)
        r.MoveSmallMotorInDegrees(90, 500)
        r.TurnInPlace(-45)
        r.DriveForDistance(290)
        r.TurnInPlace(-95)
        r.DriveForDistance(-70)
        # Seaweed mission
        Missions.Seaweed(r)
        r.TurnInPlace(-90)
        r.DriveForDistance(700)
        # Home location

    def Two(r:Robot):
        # Home location
        r.TurnInPlace(-45)
        r.DriveForDistance(130) 
        r.TurnInPlace(45)
        r.MoveSmallMotorUntilStalled(500)
        r.MoveSmallMotorInDegrees(-90, 500)
        r.DriveForDistance(770)
        # Whales mission
        Missions.Whales(r, 1)
        r.TurnInPlace(-20)
        r.DriveForDistance(-700)
        # Home location
        
    def Three(r:Robot):
        Missions.Octopus(r)

    def Four(r:Robot):
        # Home location
        r.TurnInPlace(-55)
        # Anglerfish Mission
        Missions.AnglerFish(r)
        r.TurnInPlace(-35)
        r.DriveForDistance(-180)
        # Octopus in the circle
        r.MoveBigMotorInDegrees(-90)
        # Sample to Away location
        r.TurnInPlace(15)
        r.DriveForDistance(340)
        r.TurnInPlace(-60)
        r.DriveForDistance(1000)
        # Away Location

    def Five(r:Robot):
        # Away Location
        r.TurnInPlace(40)
        r.DriveForDistance(110)
        r.MoveBigMotorUntilStalled(-500)
        r.MoveBigMotorInDegrees(20)
        r.MoveSmallMotorUntilStalled(-500)
        r.MoveSmallMotorInDegrees(20)
        r.TurnInPlace(-40)
        r.DriveForDistance(450)
        r.MoveSmallMotorInDegrees(90)
        r.DriveForDistance(30)
        r.MoveBigMotorInDegrees(75)
        
        # Coral Nursery Mission
        # Missions.CoralNursery(r)
        r.DriveForDistance(-800)
        # Shark Mission
        Missions.Shark(r)
        r.DriveForDistance(-1000)
        # Away Location

    def Six(r:Robot):
        # Away Location
        r.DriveForDistance(550)
        r.DriveForDistance(-550)
        # Coral Reef Mission
        # Missions.CoralReef(r)

        # Away Location

    def Seven(r:Robot):
        # Away Location
        r.TurnInPlace(35)
        r.DriveForDistance(350)
        r.MoveSmallMotorUntilStalled(-500)
        r.MoveSmallMotorInDegrees(90)
        r.TurnInPlace(-35)
        r.DriveForDistance(450)
        r.TurnInPlace(-40)
        r.DriveForDistance(15)
        r.MoveSmallMotorInDegrees(-100, 900)
        wait(500)
        r.MoveSmallMotorInDegrees(50)
        r.DriveForDistance(-100)
        r.MoveSmallMotorInDegrees(30)
        r.DriveForDistance(100)
        r.TurnInPlace(-50)
        r.DriveForDistance(40)
        r.MoveSmallMotorInDegrees(100)
        r.DriveForDistance(-140)
        r.TurnInPlace(-70)
        r.DriveForDistance(1000)
        # Away Location

    def Eight(r:Robot):
        # Away Location
        r.TurnInPlace(75)
        r.DriveForDistance(1080)
        r.MoveBigMotorInDegrees(-180)
        r.DriveForDistance(40)
        r.TurnInPlace(-50)
        # Second Whale Mission
        # Missions.Whales(r, 2)
        r.DriveForDistance(450)
        r.TurnInPlace(-95)
        r.DriveForDistance(500)
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