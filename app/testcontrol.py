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




p1 = Point(200., -45.)
p2 = Point(400., 45.)
p3 = Point(300., 180.)

print(p1.getCartesian())

print(np.cos(-3.14))

m = Map([p1, p2, p3])
image = m.getQImage()

image.save("test/testmap.png")


