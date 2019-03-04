import numpy as np
from PyQt5.QtGui import QPainter, QPen, QColor, QImage, QFont, QStaticText
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
        #print("x: ",x)
        y = self.value * np.cos(radangle)
        #print("y: ",y)
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
        self.area = 0
        
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

    def getQImage(self):
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
            halfheight = round(max(minx, maxx, miny, maxy)) + frame
            halfwidth = round(350 * halfheight / 180)

            #coordinates translation, _tr = translated
            xlist_tr = halfwidth + self.xlist
            ylist_tr = halfheight - self.ylist

            self.mapImage = QImage((2 * halfwidth), (2 * halfheight), QImage.Format_RGB32)
            self.mapImage.fill(Qt.white)

            #image drawing
            painter = QPainter(self.mapImage)
            painter.setRenderHint(QPainter.Antialiasing)
            pen = QPen(Qt.blue, 10, Qt.SolidLine, Qt.SquareCap, Qt.RoundJoin)
            painter.setPen(pen)

            #connecting points
            for it in range(len(xlist_tr)-1):
                painter.drawLine(round(xlist_tr[it]), round(ylist_tr[it]), round(xlist_tr[it+1]), round(ylist_tr[it+1]))
            
            painter.drawLine(round(xlist_tr[-1]), round(ylist_tr[-1]), round(xlist_tr[0]), round(ylist_tr[0]))

            #scale drawing
            # painter.setFont(QFont("Times", 9))
            # m1 = QStaticText("1m")
            # m1.prepare()
            # painter.drawStaticText(200, 200, m1)
            painter.drawLine(50, 50, 150, 50)
            painter.drawLine(50, 50, 50, 150)

            #position of the device
            pen.setColor(Qt.red)
            pen.setWidth(10)
            painter.setPen(pen)
            painter.drawPoint(round(halfwidth), round(halfheight))

            #calculation of area, sum of triangles, first point is the origin #TODO check if works
            self.area = 0

            #print("orign: ", self.xlist[0], self.ylist[0])
            for ite in range(1, len(self.xlist)-1):
                #vectors of triangle
                #print("first point: ", self.xlist[ite], self.ylist[ite])
                a_x = self.xlist[ite] - self.xlist[0]
                a_y = self.ylist[ite] - self.ylist[0]

                #print("second point: ", self.xlist[ite+1], self.ylist[ite+1])
                b_x = self.xlist[ite+1] - self.xlist[0]
                b_y = self.ylist[ite+1] - self.ylist[0]

                # print("a vector x,y: ", a_x, a_y)
                # print("b vector x,y: ", b_x, b_y)

                #magnitude of cross product, divided by 2 at the end
                self.area = self.area + (a_x * b_y) - (a_y * b_x)
                print("area so far: ", self.area)

            self.area = abs(self.area / 2.)

        return self.mapImage, self.area


class DataProcessing:
    """
    One instance class to handle data processing such as calculating errors,
    average, distance, create a map
    """
    #constants:
    error_motor_angle = 0.045 #TODO verify the value, if changed - change in hardwarecontrol
    def __init__(self):
        pass
    
    def analyseValues(self, list):
        """
        Averages the values and calculates the standard error of the list.
        return average_value, standard_error
        """
        #average of measurements
        result = sum(list) / len(list)
        #corrected sample standard deviation, degrees of freedom = 1
        stddev = np.std(list, ddof = 1)

        #estimated standard error:
        error = stddev / np.sqrt(len(list)) + (0.01 * result)
        return (result, error)

    def getWidth(self, a, b):
        """
        Calculates and returns the distance between 2 points.
        It also calculates the distance to the line made by those 2 points.
        return width, error, distance
        """
        angle = np.deg2rad(abs(a.angle - b.angle))
        costerm = 2 * a.value * b.value * np.cos(angle)
        print("costerm", costerm)
        sqwidth = a.value**2 + b.value**2 - costerm # a^2 + b^2 - 2*a*b*cos(angle<ab>)
        width = np.sqrt(sqwidth)
        
        #calculating perpendicular distance to the object
        ob = a.value + b.value + width
        twicearea = np.sqrt(ob * (ob - 2 * a.value) * (ob - 2 * b.value) * (ob - 2 * width))
        distance = twicearea / (2*width)

        #error propagation for width
        sqerror = (a.value**2) * (b.value**2) * (self.error_motor_angle**2) * (np.sin(angle)**2)\
                        + (a.error**2) * ((a.value - b.value * np.cos(angle))**2)\
                        + (b.error**2) * ((b.value - a.value * np.cos(angle))**2)
        werror = np.sqrt(sqerror/sqwidth)
                        
        
        return (width, werror, distance)


