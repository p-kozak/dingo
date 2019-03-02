import numpy as np
from PyQt5.QtGui import QPixmap, QPainter, QPen, QColor, QImage
from PyQt5.QtCore import Qt

class Point:
    """
    Class used for storing points in polar coordinates.
    Angle is in respect to the front of the device.
    """

    def __init__(self, valuepassed=0, anglepassed=0, errorpassed=0, isaWidth=False):
        self.value = valuepassed
        self.angle = anglepassed
        self.error = errorpassed
        if isaWidth:
            self.objectType = "width"
        else:
            self.objectType = "point"
    
    def getCartesian(self):
        """
        Returns the cartesian coordinates of the point.
        """
        radangle = np.deg2rad(self.angle)
        x = self.value * np.cos(radangle)
        y = self.value * np.sin(radangle)
        return (x, y)

class Map:
    """
    Class used to store list of points in cartesian coordinates, where the device is an origin.
    """
    def __init__(self, listofcartesianpoints = []):
        self.objectType = "map"
        self.pointlist = listofcartesianpoints
        self.xlist = []
        self.ylist = []
        
        self.createMap(self.pointlist)

        self.mapImage = QImage()

    def createMap(self, listofcartesianpoints):
        """
        Creates a proper map with straight walls from given list.
        Returns two lists, one consists of x values, one of y values.
        """
        for spoint in self.pointlist:
            xtemp, ytemp = spoint.getCartesian()
            self.xlist.append(xtemp)
            self.ylist.append(ytemp)
        return (self.xlist, self.ylist)

    def getQImage(self): #TODO incorporate the scaling
        """
        Returns scaled QImage of the map
        """
        #TODO better determine the dimensions of the map, FIXME fix drawing the map
        #TODO add drawing where the device is?

        minx = min(min(self.xlist), 0)
        maxx = max(max(self.xlist), 0)

        miny = min(min(self.ylist), 0)
        maxy = max(max(self.ylist), 0)

        print("before transformation:")
        print("xlist: ", self.xlist)
        print("ylist: ", self.ylist)

        #list transformation to different origin
        self.xlist = (self.xlist - minx) + 10.
        self.ylist = (self.ylist - miny) + 10.

        print("minx: ", minx)
        print("miny: ", miny)

        print("after transformation:")
        print("xlist: ", self.xlist)
        print("ylist: ", self.ylist)

        print("minx: ", minx)
        print("miny: ", miny)

        width = round((maxx - minx)) + 20
        height = round((maxy - miny)) + 20

        print("width: ", width)
        print("height: ", height)
        print("minx: ", minx)
        print("miny: ", miny)
        print("device x,y: ", (abs(minx)+10.), (abs(miny)+10.))

        self.mapImage = QImage(width, height, QImage.Format_RGB32)
        self.mapImage.fill(Qt.white)

        #image drawing
        painter = QPainter(self.mapImage)
        pen = QPen(Qt.blue, 2, Qt.SolidLine, Qt.SquareCap, Qt.RoundJoin)
        painter.setPen(pen)


        #connecting points
        for it in range(len(self.xlist)-1):
            painter.drawLine(round(self.xlist[it]), round(self.ylist[it]), round(self.xlist[it+1]), round(self.ylist[it+1]))
        
        painter.drawLine(round(self.xlist[-1]), round(self.ylist[-1]), round(self.xlist[0]), round(self.ylist[0])) 

        #position of the device
        pen.setColor(Qt.red)
        pen.setWidth(5)
        painter.setPen(pen)
        painter.drawLine(0, 0, 100, 100) #TODO test case, 
        painter.drawPoint((abs(minx)+10.), (abs(miny)+10.)) 
        painter.drawImage
        return self.mapImage


class DataProcessing:
    """
    One instance class to handle data processing such as calculating errors,
    average, distance, create a map
    """
    error_motor_angle = 0.045 #TODO verify the value
    def __init__(self):
        pass
    
    def analyseValues(self, list):
        """
        Averages the values and calculates the standard error of the list.
        return average_value, standard_error
        """
        result = sum(list) / len(list)
        #corrected sample standard deviation, degrees of freedom = 1
        stddev = np.std(list, ddof = 1)
        #estimated standard error:
        error = stddev / np.sqrt(len(list)) #TODO divide by sqrt of len(list)
        return (result, error)

    def getWidth(self, a, b):
        """
        Calculates and returns the distance between 2 points.
        return width, error
        """
        angle = abs(a.angle - b.angle)
        costerm = 2 * a.value * b.value * np.cos(np.deg2rad(angle))
        print("costerm", costerm)
        width = np.sqrt(a.value**2 + b.value**2 - costerm) # a^2 + b^2 - 2*a*b*cos(angle<ab>)
        

        #error propagation TODO: make it work
        asqerror = 2. * a.error  / a.value
        print("asqerror:", asqerror)
        bsqerror = 2. * b.error / b.value
        print("bsqerror:", bsqerror)
        costermerror_squared =  a.error/a.value + b.error / b.value + np.sqrt(2.) * self.error_motor_angle * np.tan(np.deg2rad(angle))
        print("cos term error", costermerror_squared)
        werror = (asqerror * a.value)**2 + (bsqerror * b.value)**2 #+ (costermerror_squared*(costerm**2))
        return (width, werror)


