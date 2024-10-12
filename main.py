from pybricks.pupdevices import Motor, Button
from pybricks.parameters import Port, Color, Icon
from pybricks.tools import wait, Matrix, StopWatch
from pybricks.hubs import PrimeHub

hub = PrimeHub()

def Pause(time:float):
    wait(time*1000)

# Define the Robot
class Motors:
    #DRIVE MOTORS: Left (A) Right (B) Big (E) Small (F)
    leftDrive = Motor(Port.A)
    rightDrive = Motor(Port.B)
    big = Motor(Port.E)
    small = Motor(Port.F)

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

def Forward(distance:float):
    Motors.leftDrive.run_angle(speed=distance, wait=False)
    Motors.rightDrive.run_angle(speed=distance)
    Pause(1)

def run1():
    Forward()

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
    hub.display.off()
    hub.display.number(number)

def StatusLight(color:Color):
    hub.light.off()
    hub.light.on(color)

current_selection = 0

StatusLight(Color.GREEN)
hub.display.off()

while True:
    while True:
        if Button.LEFT in hub.buttons.pressed():
            current_selection = (current_selection - 1) % 7
            break

        elif Button.RIGHT in hub.buttons.pressed():
            current_selection = (current_selection + 1) % 7
            break

        elif Button.CENTER in hub.buttons.pressed():
            # run current selection
            StatusLight(Color.YELLOW)
            hub.display.animate(Animations.running, 30)
            print(f"Running {current_selection + 1}...")
            start_time = StopWatch.time()
            eval(f'run{str(current_selection + 1)}()')
            print(f"Done running {current_selection + 1}. Time: {StopWatch.time() - start_time}")
            StatusLight(Color.GREEN)
            break
    
    # wait until there are no buttons pressed
    while not hub.buttons.pressed() == []:
        Pause(0.01)
    
    # display current selection
    DisplayNumber(current_selection + 1)
    
    
    
        
    