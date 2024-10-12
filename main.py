from pybricks.pupdevices import Motor, Button
from pybricks.parameters import Port
from pybricks.tools import wait
from pybricks.hubs import PrimeHub

def Pause(time:float):
    wait(time*1000)

# Define the Robot
class Motors:
    #DRIVE MOTORS: Left (A) Right (B) Big (E) Small (F)
    leftDrive = Motor(Port.A)
    rightDrive = Motor(Port.B)
    big = Motor(Port.E)
    small = Motor(Port.F)

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
    PrimeHub.display.off()
    PrimeHub.display.number(number)
    Pause(1)

current_selection = 0
while True:
    while True:
        if Button.LEFT in PrimeHub.buttons.pressed():
            current_selection = (current_selection - 1) % 7
            break

        elif Button.RIGHT in PrimeHub.buttons.pressed():
            current_selection = (current_selection + 1) % 7
            break

        elif Button.CENTER in PrimeHub.buttons.pressed():
            # run current selection
            eval(f'run{str(current_selection + 1)}()')
            break
    
    # wait until there are no buttons pressed
    while not PrimeHub.buttons.pressed() == []:
        Pause(0.01)
    
    # display current selection
    DisplayNumber(current_selection + 1)
    
    
    
        
    