from pybricks.pupdevices import Motor, Button
from pybricks.parameters import Port, Color, Icon
from pybricks.tools import wait, Matrix, StopWatch
from pybricks.robotics import DriveBase
from pybricks.hubs import PrimeHub

# Define the Robot
class Robot:
    #DRIVE MOTORS: Left (A) Right (B) Big (E) Small (F)
    leftDrive = Motor(Port.A)
    rightDrive = Motor(Port.B)
    big = Motor(Port.E)
    small = Motor(Port.F)
    # fix these values (measurements from the robot itself)
    # axle track is distance between the wheels
    driveBase = DriveBase(leftDrive, rightDrive, wheel_diameter=56, axle_track=105)
    driveBase.use_gyro(True)
    hub = PrimeHub()

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

def run1():
    Robot.driveBase.straight(100)

def run2():
    pass

def run3():
    pass

def run4():
    pass

def run5():
    pass

def run6():
    pass

def run7():
    pass

def DisplayNumber(number:int):
    Robot.hub.display.off()
    Robot.hub.display.number(number)

def StatusLight(color:Color):
    Robot.hub.light.off()
    Robot.hub.light.on(color)

def Rescale(value, in_min, in_max):
    neg = value / abs(value) # will either be 1 or -1
    value = abs(value)
    if value < in_min: value = in_min
    if value > in_max: value = in_max
    retvalue = (value - in_min) * (100 / (in_max - in_min))
    if retvalue > 100: retvalue = 100
    if retvalue < 0: retvalue = 0
    return retvalue * neg

current_selection = 0

StatusLight(Color.GREEN)
Robot.hub.display.off()

# display battery of hub
v = 7900
vPct = Rescale(v, 7000, 8000)
print(f"Battery %: {vPct}")
if vPct < 70:
    print("Battery is below 70% Please charge!")

while True:
    while True:
        if Button.LEFT in Robot.hub.buttons.pressed():
            current_selection = (current_selection - 1) % 7
            break

        elif Button.RIGHT in Robot.hub.buttons.pressed():
            current_selection = (current_selection + 1) % 7
            break

        elif Button.CENTER in Robot.hub.buttons.pressed():
            # run current selection
            StatusLight(Color.YELLOW)
            Robot.hub.display.animate(Animations.running, 30)
            print(f"Running {current_selection + 1}...")
            start_time = StopWatch.time()
            eval(f'run{str(current_selection + 1)}()')
            print(f"Done running {current_selection + 1}. Time: {StopWatch.time() - start_time}")
            StatusLight(Color.GREEN)
            break
    
    # wait until there are no buttons pressed
    while not Robot.hub.buttons.pressed() == []:
        wait(10)
    
    # display current selection
    DisplayNumber(current_selection + 1)