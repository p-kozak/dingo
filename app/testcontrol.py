#from control import *
from dataprocessing import *
from control import Control
import time


# x = Point(150, 0)
# x.error = 3
# y = Point(350, 0)
# y.errror = 7

# data = DataProcessing()

# width, werror = data.getWidth(x, y)
# print(width, werror)

con = Control()
# p1 = Point(200, -45)
# p2 = Point(200, 45)
# m = Map([p1, p2])
# image = m.getQImage()

# image.save("test/testmap.png")

con.moveRightStart()

time.sleep(5)
con.moveRightStop()

del con



