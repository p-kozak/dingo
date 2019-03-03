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
        x = self.value * np.sin(radangle)
        print("x: ",x)
        y = self.value * np.cos(radangle)
        print("y: ",y)
        return (x, y)

class Map:
    """
    Class used to store list of points in cartesian coordinates, where the device is an origin.
    """
    def __init__(self, listofpoints = []):
        self.objectType = "map"
        self.pointlist = listofpoints
        self.xlist = []
        self.ylist = []
        self.mapImage = QImage()
        
        if len(self.pointlist) != 0:
            self.createMap(self.pointlist)
            self.getQImage()

        


    def createMap(self, listofpoints=[]):
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
        Creates Qimage of the map.
        Returns scaled QImage of the map
        """
        if self.mapImage.isNull():
            #determining size of image
            minx = abs(min(self.xlist))
            maxx = abs(max(self.xlist))

            miny = abs(min(self.ylist))
            maxy = abs(max(self.ylist))

            frame = 10
            halfsize = round(max(minx, maxx, miny, maxy)) + frame

            #coordinates translation
            self.xlist = halfsize + self.xlist
            self.ylist = halfsize - self.ylist

            self.mapImage = QImage(int(700 * 2* halfsize / 360), (2 * halfsize), QImage.Format_RGB32)
            self.mapImage.fill(Qt.white)

            #image drawing
            painter = QPainter(self.mapImage)
            pen = QPen(Qt.blue, 5, Qt.SolidLine, Qt.SquareCap, Qt.RoundJoin)
            painter.setPen(pen)

            #connecting points
            for it in range(len(self.xlist)-1):
                painter.drawLine(round(self.xlist[it]), round(self.ylist[it]), round(self.xlist[it+1]), round(self.ylist[it+1]))
            
            painter.drawLine(round(self.xlist[-1]), round(self.ylist[-1]), round(self.xlist[0]), round(self.ylist[0])) 

            #position of the device
            pen.setColor(Qt.red)
            pen.setWidth(5)
            painter.setPen(pen)
            painter.drawPoint(round(halfsize), round(halfsize))

            #calculation of area

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
        It also calculates the distance to the line made by those 2 points.
        return width, error, distance
        """
        angle = abs(a.angle - b.angle)
        costerm = 2 * a.value * b.value * np.cos(np.deg2rad(angle))
        print("costerm", costerm)
        width = np.sqrt(a.value**2 + b.value**2 - costerm) # a^2 + b^2 - 2*a*b*cos(angle<ab>)
        

        ob = a.value + b.value + width
        twicearea = np.sqrt(ob * (ob - 2 * a.value) * (ob - 2 * b.value) * (ob - 2 * width))
        distance = twicearea / width

        #TODO add distance to the object

        #error propagation TODO: make it work
        asqerror = 2. * a.error  / a.value
        print("asqerror:", asqerror)
        bsqerror = 2. * b.error / b.value
        print("bsqerror:", bsqerror)
        costermerror_squared =  a.error/a.value + b.error / b.value + np.sqrt(2.) * self.error_motor_angle * np.tan(np.deg2rad(angle))
        print("cos term error", costermerror_squared)
        werror = (asqerror * a.value)**2 + (bsqerror * b.value)**2 #+ (costermerror_squared*(costerm**2))
        return (width, werror, distance)


