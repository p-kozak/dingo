from PyQt5.QtCore import QObject, qDebug, pyqtSignal, QTimer
from hardwarecontrol import HardwareControl
from dataprocessing import Point, Map, DataProcessing
import time



class Control(QObject):
    """
    One-instance class that handles processing of data and hardware interaction.
    """
    #Signals for sending data to gui
    sendPointSignal = pyqtSignal(Point)
    sendMapSignal = pyqtSignal(Map)
    
    
    def __init__(self):
        QObject.__init__(self)
        self.prevpoint = Point()
        self.prevprevpoint = Point()
        self.hardware = HardwareControl()
        self.data = DataProcessing()

        self.motorTimer = QTimer(self)
        self.basemotorstep = 1

        self.motorbasepause = 5
        self.motorpause = 5*self.motorbasepause
        
        self.motorTimer.timeout.connect(self.motorStep)

    def __del__(self):
        self.motorTimer.stop()
    
    def motorStep(self):
        self.hardware.turnMotor(self.basemotorstep, True)

	#These are slots which receive signal from GUI
    def toggleLaser(self):
        """Toggles the laser on and off"""
        self.hardware.toggleLaser()		
        return 

    def moveRightStart(self):
        """Starts movement of motor to the right until moveStop() is called"""
        self.motorTimer.stop()
        self.basemotorstep = 1
        self.motorTimer.start(self.motorpause)

    def moveRightStop(self):
        """Stops movement of motor"""
        self.motorTimer.stop()
        return

    def moveLeftStart(self):
        """Starts movement of motor to the left until moveStop() is called"""
        self.motorTimer.stop()
        self.basemotorstep = -1
        self.motorTimer.start(self.motorpause)


    def moveLeftStop(self):
        """Stops movement of motor"""
        self.motorTimer.stop()
        return
        

    def receiveSpeedValue(self, speed):
        speed = 11 - speed #there are 10 levels of speed, max is 10
        self.motorpause = speed * self.motorbasepause
        return

    def measureDistance(self):
        """Measures distance to the object, returns point to gui"""
        lval = self.hardware.getDistance()
        dist, error = self.data.analyseValues(lval)
        angle = self.hardware.Motor.angle
        self.prevprevpoint = self.prevpoint
        self.prevpoint = Point(dist, angle, error)

        self.sendPoint(self.prevpoint)
        return
    
    def setAngleToZero(self):
        """Calibrates absolute angle to be set at the current position of the motor"""
        self.hardware.calibrateMotor()
        return

    def calculateWidth(self):
        """Calculates width between last two points. Returns value to gui"""
        p = Point(isaWidth=True)
        p.value, p.error, p.angle = self.data.getWidth(self.prevpoint, self.prevprevpoint)
        #p = Point(val, 0, error, True)
        self.sendPoint(p)
    
        return 

    def getMap(self, leftAngle=-180, rightAngle=180, resolution=10):
        """
        Does scan of a room, creates Map() and image.
        Returns Map() to Gui
        """
        #turn of the laser pointer off if on
        if self.hardware.Laser.value != 0:
            self.hardware.Laser.off()

        #starting angle and angle boundaries
        startangle = self.hardware.Motor.angle

        leftbound = max((leftAngle + startangle), -180)
        rightbound = min((rightAngle + startangle), 180)

        #to minimise movement unneccesary, decide whether move first right or left
        direction = 1 if startangle >= 0 else -1

        #basestep decides on resolution of the scan, 10 lvl of resolution
        basestep = -4*direction * (11 - resolution)
        
        
        #move to the start position
        if direction == 1:
            self.hardware.turnMotor(rightAngle)
        else:
            self.hardware.turnMotor(leftAngle)

        #list to store points
        lpoint = []
        
        #do the scan
        while (self.hardware.Motor.angle < rightbound and direction == -1) or (self.hardware.Motor.angle > leftbound and direction == 1):
            print("entered scan",self.hardware.Motor.angle)
            #get distance at current position:
            lval = self.hardware.getDistance()
            #discard empty list
            if len(lval) != 0:
                dist, error = self.data.analyseValues(lval)
                angle = self.hardware.Motor.angle
                lpoint.append(Point(dist, angle, error))
            
            #move to next position
            self.hardware.turnMotor(basestep, True)

        #create a map
        print("dlugosc lpoint:", len(lpoint))
        scan = Map(lpoint)

        scan.mapImage.save("test/testdata.png") #test

        #send map to GUI
        self.sendMap(scan)

        #move back to start position
        self.hardware.turnMotor((startangle - self.hardware.Motor.angle))
        return



    def sendPoint(self, point):
        """
        Sends point to gui
        """
        self.sendPointSignal.emit(point)
        return

    def sendMap(self, map):
        """
        Sends map to gui
        """
        self.sendMapSignal.emit(map)
        return 


