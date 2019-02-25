#from control import *
from dataprocessing import *


x = Point(150, 0)
x.error = 3
y = Point(350, 0)
y.errror = 7

data = DataProcessing()

width, werror = data.getWidth(x, y)
print(width, werror)
