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

        self.motortimer = QTimer(self)
        self.basemotorstep = 1
        self.motortimer.timeout.connect(self.motorStep)
    
    def motorStep(self):
        self.hardware.turnMotor(self.basemotorstep, True)

	#These are slots which receive signal from GUI TODO
    def toggleLaser(self):
        """Toggles the laser on and off"""
        self.hardware.toggleLaser()		
        return 

    def moveRightStart(self):
        """Starts movement of motor to the right until moveStop() is called"""
        self.motortimer.stop()
        self.basemotorstep = 1
        self.motortimer.start(10)

    def moveRightStop(self):
        """Stops movement of motor"""
        self.motortimer.stop()
        return

    def moveLeftStart(self):
        """Starts movement of motor to the left until moveStop() is called"""
        self.motortimer.stop()
        self.basemotorstep = -1
        self.motortimer.start(10)


    def moveLeftStop(self):
        """Stops movement of motor"""
        self.motortimer.stop()
        return
        

    def receiveSpeedValue(self, speed):
        #Receives current speed value from GUI
        return

    def measureDistance(self):
        """Measures distance to the object, returns point to gui"""
        lval = self.hardware.getDistance()
        dist, error = self.data.analyseValues(lval)
        angle = self.hardware.Motor.angle
        self.prevprevpoint = self.prevpoint
        self.prevpoint = Point(dist, angle, error)

        self.sendPoint(self.prevpoint)

        #test case
        # point = Point()
        # point.value = 2137
        # point.objectType = "point"
        # point.angle = 21
        # point.error = 37
        # self.sendPoint(point)
        
        return
    
    def setAngleToZero(self):
        """Calibrates absolute angle to be set at the current position of the motor"""
        self.hardware.calibrateMotor()
        return

    def calculateWidth(self):
        val, error = self.data.getWidth(self.prevpoint, self.prevprevpoint)
        p = Point(val, 0, error, True)
        self.sendPoint(p)
        #test case
        # point = Point()
        # point.value = 6
        # point.objectType = "width"
        # point.angle = 56
        # point.error = 43
        # self.sendPoint(point)
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


