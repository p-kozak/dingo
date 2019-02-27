from gpiozero.pins.mock import MockFactory
from gpiozero import Device, DigitalOutputDevice
import time

class StepMotor:
    """
    One instance class to control motor via gpio 
    """
    WAIT_TIME = .001
    STEP_DEGREE = 0.05625 #uncertainty is ~0.045
    def __init__(self, currentangle=0):
        """
        Motor Setup.
        Pin layout available on https://gpiozero.readthedocs.io/en/stable/recipes.html
        """
        #TODO comment out next line if working on Raspberry Pi !!!!!!!!
        Device.pin_factory = MockFactory() 
        self.vcc = DigitalOutputDevice(26) #pin BOARD37, VCC = 0
        time.sleep(self.WAIT_TIME) #wait 1 ms
        self.mode1 = DigitalOutputDevice(19, initial_value = True) #pin BOARD35, MODE1 = 1
        self.mode2 = DigitalOutputDevice(13, initial_value = True) #pin BOARD33, MODE2 = 1
        self.stck = DigitalOutputDevice(6, initial_value = True) #pin BOARD31, STCK = 1
        self.dir = DigitalOutputDevice(5) #pin BOARD29, DIR = 0
        time.sleep(self.WAIT_TIME) #wait 1 ms
        self.vcc.on() #VCC = 1
        self.stck.on() #STCK = 0

        self.angle = currentangle #current angle of the motor
        self.direction = 1 #1 for right turn, -1 for left turn.

    def turnbyStep(self, stepnum=5, steptime=WAIT_TIME): #TODO make it turn backwards if stepnum <0, make 2 speeds 
        """
        Move by specified amount of steps, 1 step is 0.05625 degrees
        1 step is 1 full clock, min high time is 1 ms.
        return current angle of motor
        """
        if stepnum >=0 and self.direction == -1:
            self.dir.off() #right turn DIR = 0
            self.direction = 1
        elif stepnum <=0 and self.direction == 1:
            self.dir.on() #left turn DIR = 1
            self.direction = -1


        if steptime < self.WAIT_TIME:
            steptime = self.WAIT_TIME

        stepnum = abs(stepnum)

        for it in range(stepnum):
            self.stck.on()
            time.sleep(steptime)
            self.stck.off()
            time.sleep(steptime)

        self.angle = self.angle + self.STEP_DEGREE*self.direction*stepnum
        return self.angle




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
        self.motorangle = self.Motor.angle

    def turnMotor(self, degrees, stepInsteadofDeg = False): #TODO add speed of turning
        """
        Turns motor and returns the angle TODO(check how it actually should work)
        """
        if stepInsteadofDeg:
            stepnum = degrees
        else:
            stepnum = int(degrees / Motor.STEP_DEGREE)

        motangle = Motor.turnbyStep(stepnum)
        return motangle

    def calibrateMotor(self):
        """
        Changes the absolute motor angle to the current position of motor
        """
        self.Motor.angle = 0
        
