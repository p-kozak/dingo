import numpy as np

class Point:
    """
    Class used for storing points in polar coordinates.
    Angle is in respect to the front of the device.
    """

    def __init__(self, valuepassed=0, anglepassed=0, errorpassed=0):
        self.value = valuepassed
        self.angle = anglepassed
        self.error = errorpassed
    
    def getCartesian(self):
        """
        Returns the cartesian coordinates of the point.
        """
        return (x, y)

class Map:
    """
    Class used to store list of points in cartesian coordinates, where the device is an origin.
    """
    def __init__(self, listofcartesianpoints = []):
        self.pointlist = listofcartesianpoints

    def createMap(self, listofcartesianpoints):
        """
        Creates a proper map with straight walls from given list.
        """
        return mappedPoints

    def getQImage(self, scale = 0): #TODO decide on default value based on the size of the screen
        """
        Returns scaled QImage of the map
        """
        return mapImage


class DataProcessing:
    """
    One instance class to handle data processing such as calculating errors,
    average, distance, create a map
    """
    def __init__(self):
        pass
    
    def analyseValues(self, list):
        """
        Averages the values and calculates the standard error of the list
        """
        result = sum(list) / len(list)
        #corrected sample standard deviation, degrees of freedom = 1
        stddev = np.std(list, ddof = 1)
        #estimated standard error:
        error = stddev #TODO divide by sqrt of len(list)

