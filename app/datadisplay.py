from control import *
from PyQt5.QtWidgets import *
from time import gmtime, strftime
class DataDisplay(QWidget):
	def __init__(self):
		QWidget.__init__(self)
		self.initialiseScrollArea()
		self.addGridToScroll()
		layout = QVBoxLayout()
		self.setMinimumSize(800,380)
		self.setLayout(layout)
		layout.addWidget(self.scrollArea)



	def initialiseScrollArea(self):
		self.scrollArea = QScrollArea()
		self.scrollArea.setWidgetResizable(True)
		#self.scrollArea.setMinimumSize(800,380)
		return

	def addGridToScroll(self):
		gridWidget = QWidget()
		#In this case we CANNOT set size of the gridWidget: let it resize, set only size of the scrollarea
		#gridWidget.setMinimumSize(800,900)
		self.gridDataLayout = QGridLayout()
		gridWidget.setLayout(self.gridDataLayout)
		self.scrollArea.setWidget(gridWidget)

		return

	def spamButtons(self):
		#Debug function for adding buttons to the widget
		for i in range(20):
			button = QPushButton(str(i))
			button.setFixedHeight(70)
			self.gridDataLayout.addWidget(button,i,0)
		return

	def addMeasurementToDisplay(self, object):
		if object.objectType == "point":
			self.addPointToDisplay(object)
		elif object.objectType == "width":
			self.addWidthToDisplay(object)

	def addPointToDisplay(self,object):
		self.addTimeBoxToDisplay()
		self.addTypeBoxToDisplay("DISTANCE")
		self.addDistanceBoxToDisplay(object.value)
		self.addAngleBoxToDisplay(object.angle)
		self.addErrorBoxToDisplay(object.error)
		return

	def addWidthToDisplay(self,object):
		self.addTimeBoxToDisplay()
		self.addTypeBoxToDisplay("WIDTH")
		self.addWidthBoxToDisplay(object.value)
		self.addErrorBoxToDisplay(object.error)
		return
			
	def addTimeBoxToDisplay(self):
		boxTime = QLineEdit()
		boxTime.setFixedHeight(30)
		boxTime.setFixedWidth(200)
		boxTime.setReadOnly(True)
		boxTime.setText(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
		self.gridDataLayout.addWidget(boxTime, self.gridDataLayout.rowCount(), 0 )
		return 

	def addTypeBoxToDisplay(self, type):
		boxType = QLineEdit()
		boxType.setFixedHeight(30)
		boxType.setFixedWidth(90)
		boxType.setReadOnly(True)
		boxType.setText(type)
		self.gridDataLayout.addWidget(boxType, self.gridDataLayout.rowCount() -1 ,1)
		return

	def addDistanceBoxToDisplay(self, value):
		boxDistance = QLineEdit()
		boxDistance.setFixedHeight(30)
		boxDistance.setFixedWidth(90)
		boxDistance.setReadOnly(True)
		boxDistance.setText("Distance: " + str(value))
		self.gridDataLayout.addWidget(boxDistance, self.gridDataLayout.rowCount() -1 ,2)
		return 

	def addAngleBoxToDisplay(self, angle):
		boxAngle = QLineEdit()
		boxAngle.setFixedHeight(30)
		boxAngle.setFixedWidth(90)
		boxAngle.setReadOnly(True)
		boxAngle.setText("Angle: " + str(angle))
		self.gridDataLayout.addWidget(boxAngle, self.gridDataLayout.rowCount() -1 ,3)
		return

	def addErrorBoxToDisplay(self, error):
		boxError = QLineEdit()
		boxError.setFixedHeight(30)
		boxError.setFixedWidth(90)
		boxError.setReadOnly(True)
		boxError.setText("Error: " + str(error))
		self.gridDataLayout.addWidget(boxError, self.gridDataLayout.rowCount() -1 ,4)
		return

	def addWidthBoxToDisplay(self, width):
		boxError = QLineEdit()
		boxError.setFixedHeight(30)
		#boxError.setFixedWidth(180)
		boxError.setReadOnly(True)
		boxError.setText("Width: " + str(width))
		self.gridDataLayout.addWidget(boxError, self.gridDataLayout.rowCount() -1 , 2 ,1 ,2 )
		return







