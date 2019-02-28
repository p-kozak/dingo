from PyQt5.QtCore import QObject, qDebug, pyqtSignal
from hardwarecontrol import HardwareControl
from dataprocessing import Point, Map, DataProcessing



class Control(QObject):
 
    #Signals for sending data to gui
    sendPointSignal = pyqtSignal(Point)
    sendMapSignal = pyqtSignal(Map)
    """
    One-instance class that handles processing of data and hardware interaction.
    """
    
    def __init__(self):
        QObject.__init__(self)
        self.angleabs = 0
        self.anglecurrent = 0
        self.prevpoint = Point()
        self.prevprevpoint = Point()
        self.hardware = HardwareControl()
        self.data = DataProcessing()
        self.motormoving = False
    


	#These are slots which receive from engine TODO
    def toggleLaser(self):
        """Toggles the laser on and off"""
        self.hardware.toggleLaser()		
        return 

    def moveRightStart(self):
        """Starts movement of motor to the right until moveStop() is called"""
        self.motormoving = True
        while self.motormoving:
            self.hardware.turnMotor(5, stepInsteadofDeg=True)
        return

    def moveRightStop(self):
        """Stops movement of motor"""
        self.motormoving = False
        return

    def moveLeftStart(self):
        """Starts movement of motor to the left until moveStop() is called"""
        self.motormoving = True
        while self.motormoving:
            self.hardware.turnMotor(5, stepInsteadofDeg=True)
        return

    def moveLeftStop(self):
        """Stops movement of motor"""
        self.motormoving = False
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
        """Calculates width between last two points. Returns value to gui"""
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


