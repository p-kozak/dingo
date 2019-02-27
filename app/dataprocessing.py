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
        self.objectType = "point"
    
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
        self.objectType = "map"

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
    error_motor_angle = 0.01 #TODO get a correct value
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
        asqerror = 2 * a.error  / a.value
        print("asqerror:", asqerror)
        bsqerror = 2 * b.error / b.value
        print("bsqerror:", bsqerror)
        costermerror_squared =  a.error/a.value + b.error / b.value + np.sqrt(2) * self.error_motor_angle * np.tan(np.deg2rad(angle))
        print("cos term error", costermerror_squared)
        werror = (asqerror * a.value)**2 + (bsqerror * b.value)**2 #+ (costermerror_squared*(costerm**2))
        return (width, werror)


