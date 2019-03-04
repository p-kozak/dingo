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
print("started")
p1 = Point(200., -45.)
p2 = Point(200., 45.)
p3 = Point(300., 180.)

l = [p1, p2, p3]
print("here")
m = Map([p1, p2, p3])
image, area = m.mapImage, m.area
print("area: ", area)
image.save("test/testmap.png")


#test for text drawing
# mapImage = QImage(1000, 1000, QImage.Format_RGB32)
# mapImage.fill(Qt.white)

# painter = QPainter(mapImage)
# pen = QPen(Qt.blue, 5, Qt.SolidLine, Qt.SquareCap, Qt.RoundJoin)
# painter.setPen(pen)

# painter.setFont(QFont("Times", 2))
# painter.drawText(100, 100, "m")

# mapImage.save("test/testmap.png")