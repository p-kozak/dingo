from PyQt5.QtCore import QObject, qDebug
from hardwarecontrol import *
from dataprocessing import *



class Control(QObject):

    #Signals for sending data to gui
    sendPointSignal = pyqtSignal(Point)
    sendMapSignal = pyqtSignal(Map)
    sendWidthSignal = pyqtSignal(int)
    """
    One-instance class that handles processing of data and hardware interaction.
    """
    
    def __init__(self):
        QObject.__init__(self)
        self.angleabs = 0
        self.anglecurrent = 0
        self.prevpoint = Point()
        self.prevprecpoint = Point()
        self.hcontrol = HardwareControl()


    def getLidar():
        """
        Obtains single value of measurement from LIDAR sensor
        """
        return value_from_LIDARsensor

    def moveMotorBynStep(self, stepnum):
        """
        Moves motor by number of basic steps
        """
        return angle_moved_by


    def getDistance(self, samplesize=10):
        """
        takes n = 10 ( //TODO specify appropiate number)
        measurements and returns them as a list
        """
        l = []
        for it in range(samplesize):
            l[it] = getLidar()
        return l

    def calibrateMotor(self):
        """
        Sets current absolute angle to 0
        """
        self.angleabs = 0
        self.anglecurrent = 0
        return
    
 
        
    def getWidth(self, A, B):
        """
        Accepts class point as arguments
        Calculates the distance between 2 points and error of the calculation.
        Returns both values.
        """
        return width, errorwidth


    def analyseMeasurement(self, list = []):
        """
        Performs mathematical analysis of set of measuerent.
        Returns calculated value and its error.
        """
        return (value, errorvalue)
      


	#These are slots which receive from engine
    def toggleLaser(self):
        """Toggles the laser on and off"""		
        return 

    def moveRightStart(self):
        """Starts movement of motor to the right until moveStop() is called"""
        return

    def moveRightStop(self):
        """Stops movement of motor"""
        return

    def moveLeftStart(self):
        """Starts movement of motor to the left until moveStop() is called"""
        return

    def moveLeftStop(self):
        """Stops movement of motor"""
        return

    def measureDistance(self):
        """Measures distance to the object"""
        return
    
    def setAngleToZero(self):
        """Calibrates absolute angle to be set at the current position of the motor"""
        return

    def calculateWidth(self):
        """Calls getWidth() which returns distanmce bewteen last 2 measured points"""
        return 


    def sendPoint(self, point):
        self.sendPointSignal.emit(point)
        return

    def sendMap(self, map):
        self.sendMapSignal.emit(map)
        return 

    def sendWidth(self, width):
        self.sendWidthSignal.emit(width)
