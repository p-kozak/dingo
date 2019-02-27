#from control import *
from dataprocessing import *
from control import Control


x = Point(150, 0)
x.error = 3
y = Point(350, 0)
y.errror = 7

data = DataProcessing()
con = Control()

width, werror = data.getWidth(x, y)
print(width, werror)
