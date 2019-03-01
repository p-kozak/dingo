from gpiozero.pins.mock import MockFactory
from gpiozero import Device, DigitalOutputDevice
import serial
import time


#constants for Lidar() TODO try to put them inside the class
cfgheader = [0x42, 0x57, 0x02, 0x00]  
cfgenter = [0x00, 0x00, 0x01, 0x02]
cfgexit = [0x00, 0x00, 0x00, 0x02]
cfgrst = [0xFF, 0xFF, 0xFF, 0xFF]
cfginterval = [0x01, 0x00, 0x00, 0x07]
cfgmm = [0x00, 0x00, 0x00, 0x1A]
cfgcm = [0x00, 0x00, 0x01, 0x1A]
cfgexttrigger = [0x00, 0x00, 0x00, 0x40]
cfginttrigger = [0x00, 0x00, 0x01, 0x40]
cfggetdata = [0x00, 0x00, 0x00, 0x41]  

class LidarSensor:   
    def __init__(self, serport='/dev/ttyS0'):
        self.ser = serial.Serial(port=serport, 
                   baudrate = 115200,
                   parity=serial.PARITY_NONE,
                   stopbits=serial.STOPBITS_ONE,
                   bytesize=serial.EIGHTBITS)

        self.resultsmax = 5 # number of measurements per data packet
        self.offset = 50 # calibration offset

    def configure(self):
        self.reset()
        time.sleep(1) # wait to ensure command acknowledged
        self.setdistunit(distunit="mm")
        time.sleep(0.5)   

    def sendcmd(self, cmdbytes):
        cmdbytearray = bytearray(cmdbytes)
        self.ser.write(cmdbytearray)
    
    def reset(self):
        cmd = cfgheader + cfgrst
        self.sendcmd(cmd)

    def setinterval(self, interval=10):
        cmd = cfgheader + cfginterval
        cmd[5] = round(interval, -1) & 0xFF
        print("value: " + str(hex(cmd[5])))
        self.sendcmd(cmd)

    def setdistunit(self, distunit="mm"):
        if distunit == "cm":
            cmd = cfgheader + cfgcm
        else:
            cmd = cfgheader + cfgmm
        self.sendcmd(cmd)

    def settriggermode(self, triggermode="int"):
        if triggermode == "ext":
            cmd = cfgheader + cfgexttrigger
        else:
            cmd = cfgheader + cfginttrigger
        self.sendcmd(cmd)

    def getdata(self):
        dists = []
        for n in range(self.resultsmax):
            dist = 65535
            while dist > 12000: # any value outside the range of 300-12000 is invalid
                self.ser.flushInput()
                s = self.ser.read(9)
                if int(s[0]) == 0x59 and int(s[1]) == 0x59: # check that message contains data
                    # calculate checksum
                    checksum = 0
                    for i in range(8):
                        checksum += int(s[i])    
                    if checksum & 0xFF == int(s[8]): # checksum is valid
                        distl = int(s[2]) & 0xFF
                        disth = int(s[3]) & 0xFF
                        dist = (disth<<8) + distl - self.offset
                        if (dist < 300):
                            dist = 300
                        
            dists.append(dist)
            
        return dists

    def calibrate(self, actualdist):
        measureddists = self.getdata()
        self.offset = actualdist - sum(measureddists)/len(measureddists)



class StepMotor:
    """
    One instance class to control motor via gpio 
    """
    WAIT_TIME = .001
    STEP_DEGREE = 0.05625 #uncertainty is ~0.045
    BIG_STEP_DEGREE = 0.9
    def __init__(self, currentangle=0):
        """
        Motor Setup.
        Pin layout available on https://gpiozero.readthedocs.io/en/stable/recipes.html
        MODE1 = 1, MODE2 = 1 => microstep
        MODE1 = 0, MODE2 = 0 => normalstep
        """
        #TODO comment out next line if working on Raspberry Pi !!!!!!!!
        #Device.pin_factory = MockFactory() 
        self.vcc = DigitalOutputDevice(26) #pin BOARD37, VCC = 0
        time.sleep(self.WAIT_TIME) #wait 1 ms
        self.mode1 = DigitalOutputDevice(19, initial_value = True) #pin BOARD35, MODE1 = 1
        self.mode2 = DigitalOutputDevice(20, initial_value = True) #pin BOARD38, MODE2 = 1
        self.stck = DigitalOutputDevice(13, initial_value = True) #pin BOARD33, STCK = 1
        self.dir = DigitalOutputDevice(16) #pin BOARD36, DIR = 0
        time.sleep(self.WAIT_TIME) #wait 1 ms
        self.vcc.on() #VCC = 1
        self.stck.on() #STCK = 0

        self.angle = currentangle #current angle of the motor
        self.direction = 1 #1 for right turn, -1 for left turn.
        self.stepmicro = True #True for micro step, False for normal step

    def turnbyStep(self, stepnum=5, steptime=WAIT_TIME, stepsize=0): #TODO make it turn backwards if stepnum <0, make 2 speeds 
        """
        Move by specified amount of steps, 1 step is 0.05625 degrees
        1 step is 1 full clock, min high time is 1 ms.
        return current angle of motor
        """
        if stepsize == 0 and self.stepmicro == False: #set the microstep
            self.mode1.on()
            self.mode2.on()
        if stepsize != 0 and self.stepmicro == True: #set the normal step
            self.mode1.off()
            self.mode2.off()


        if stepnum >= 0 and self.direction == -1:
            self.dir.off() #right turn DIR = 0
            self.direction = 1
        elif stepnum <= 0 and self.direction == 1:
            self.dir.on() #left turn DIR = 1
            self.direction = -1

        print(self.direction)

        newangle =self.angle + (self.STEP_DEGREE * self.direction * stepnum)

        if newangle < 200 and newangle > -200:
            if steptime < self.WAIT_TIME:
                steptime = self.WAIT_TIME

            stepnum = abs(stepnum)

            if self.stck.value == 1:
                self.stck.off()

            for it in range(stepnum):
                self.stck.on()
                time.sleep(steptime)
                self.stck.off()
                time.sleep(steptime)
            self.angle = newangle    
        return self.angle





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

        self.Lidar = LidarSensor()
        self.Lidar.configure()

        self.Laser = DigitalOutputDevice(21) #BOARD21
        #self.motorangle = self.Motor.angle

    def turnMotor(self, degrees, stepInsteadofDeg = False, steptime=1): #TODO add speed of turning
        """
        Steptime is in miliseconds.
        Turns motor and returns the new angle of the motor.
        The motor range is limited to 200 degrees both directions.
        """
        if stepInsteadofDeg:
            stepnum = int(degrees)
        else:
            stepnum = int(degrees / self.Motor.STEP_DEGREE)

        steptime = steptime / 100
        motangle = self.Motor.turnbyStep(stepnum)
        return motangle


    def calibrateMotor(self):
        """
        Changes the absolute motor angle to the current position of motor
        """
        self.Motor.angle = 0

    def getDistance(self):
        """
        returns the distances in a list
        """
        lvalues = self.Lidar.getdata()
        return lvalues

    def toggleLaser(self):
        if self.Laser.value == 1:
            self.Laser.off()
        else:
            self.Laser.on()

        
