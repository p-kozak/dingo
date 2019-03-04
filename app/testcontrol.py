#from control import *
from dataprocessing import *
#from control import Control
import time

#test case for width calculation and error propagation
# x = Point(150, -45)
# x.error = 3
# y = Point(350, 45)
# y.errror = 7

# data = DataProcessing()

# width, werror, dist = data.getWidth(x, y)
# print(width, werror, dist)

# con = Control()


#test case for map drawing
p1 = Point(200., -45.)
p2 = Point(200., 45.)
p3 = Point(0., 0.)

l = [p1, p2, p3]

m = Map([p1, p2, p3])
image, area = m.getQImage()
print("area: ", area)
image.save("test/testmap.png")

