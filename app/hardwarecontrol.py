from gpiozero import DigitalOutputDevice
import time

class StepMotor:
    """
    One instance class to control motor via gpio 
    """
    WAIT_TIME = .001
    STEP_DEGREE = 0.9 #TODO specify the degrees for one step
    def __init__(self):
        """
        Motor Setup.
        Pin layout available on https://gpiozero.readthedocs.io/en/stable/recipes.html
        """
        self.vcc = DigitalOutputDevice("BOARD37") #VCC = 0
        time.sleep(self.WAIT_TIME) #wait 1 ms
        self.mode1 = DigitalOutputDevice("BOARD36", initial_value = True) #MODE1 = 1
        self.mode2 = DigitalOutputDevice("BOARD35", initial_value = True) #MODE2 = 1
        self.stck = DigitalOutputDevice("BOARD34", initial_value = True) #STCK = 1
        self.dir = DigitalOutputDevice("BOARD33") #DIR = 0
        time.sleep(self.WAIT_TIME) #wait 1 ms
        self.vcc.on() #VCC = 1
        self.stck.on() #STCK = 0

        self.angle = 0 #absolute angle
        self.direction = 1 #1 for right turn, -1 for left turn.

    def turnbystep(self, stepnum=5, steptime=WAIT_TIME):
        """
        Move by specified amount of steps, 1 step is 0.9 degrees
        1 step is 1 full clock, min high time is 1 ms.
        """
        if steptime < self.WAIT_TIME:
            steptime = self.WAIT_TIME

        for it in range(stepnum):
            self.stck.on()
            time.sleep(steptime)
            self.stck.off()
            time.sleep(steptime)
            self.motangle = self.angle + self.STEP_DEGREE*self.direction

    def changedirection(self):
        """
        Change the direction of motor movement.
        """
        self.direction = -self.direction
        if self.direction >= 0:
            self.dir.off()
        else:
            self.dir.on()



class Lidar:
    """
    One instance class to control the lidar
    """
    def __init__(self):
        pass




class HardwareControl:
    """
    One instance class to control and setup hardware (LIDAR sensor and motor)
    Integrates Motor and Lidar control. 
    """
    
    def __init__(self):
        """
        Setup Motor and TODO Lidar
        """
        self.Motor = StepMotor()
        self.motorangle

    def turnMotor(self, degrees):
        """
        Turns motor and returns the angle TODO(check how it actually should work)
        """
        if degrees < 0:
            self.Motor.changedirection()
            
        stepnum = abs(degrees / self.Motor.STEP_DEGREE)
        self.motorangle = self.motorangle + self.Motor.STEP_DEGREE*self.Motor.direction
        self.Motor.turnbystep(stepnum)
        

    def calibrateMotor(self):
        """
        Changes the absolute motor angle to the current position of motor
        """
        self.motorangle = 0
