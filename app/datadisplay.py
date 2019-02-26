from control import *
from PyQt5.QtWidgets import *
from time import gmtime, strftime
class DataDisplay(QWidget):
	def __init__(self):
		QWidget.__init__(self)
		# scroll = QScrollArea()
		# scroll.setWidgetResizable(True) # CRITICAL
		# scroll.setMinimumSize(800,380)
		# inner = QWidget()
		# layout = QVBoxLayout()
		# inner.setLayout(layout)
		# scroll.setWidget(inner) # CRITICAL

		# for i in range(10):
		#     b = QPushButton("dupa")
		#     layout.addWidget(b)
		# scroll.show()


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
		print("dupa 5")
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
			addPointToDisplay(object.type)
		elif object.type == "width":
			addWidthToDisplay(object.type)

	def addPointToDisplay(self,object):
		self.addTimeBoxToDisplay()
		self.addTypeBoxToDisplay("POINT")
		self.addDistanceBoxToDisplay(object.value)
		self.addAngleBoxToDisplay(object.angle)
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
		boxDistance.setText("DISTANCE: " + str(value))
		self.gridDataLayout.addWidget(boxDistance, self.gridDataLayout.rowCount() -1 ,2)
		return 

	def addAngleBoxToDisplay(self, angle):
		boxAngle = QLineEdit()
		boxAngle.setFixedHeight(30)
		boxAngle.setFixedWidth(90)
		boxAngle.setReadOnly(True)
		boxAngle.setText("ANGLE: " + str(angle))
		self.gridDataLayout.addWidget(boxAngle, self.gridDataLayout.rowCount() -1 ,3)
		return





