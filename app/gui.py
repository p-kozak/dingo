from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread
from control import Control
from comms import Comms


class MainWindow(QMainWindow): 
	def __init__(self, parent = None):
		QMainWindow.__init__(self)
		#Set the properties of the window
		self.setMinimumSize(800,480)
		self.setWindowTitle("Dingo is amazing")
		
		#test code just to put something on the grid
		mainWidget = QWidget()
		mainLayout = QHBoxLayout()
		mainWidget.setLayout(mainLayout)
		self.setCentralWidget(mainWidget)

		#Layout and widget for the left part of the GUI - buttons
		gridWidget = QWidget()
		gridWidget.setMinimumSize(280,480)
		gridLayout = QGridLayout()
		gridWidget.setLayout(gridLayout)
		mainLayout.addWidget(gridWidget)



		#Prototype layout and widget for the right part of the GUI- display
		horWidget = QWidget()
		horWidget.setMinimumSize(520,480)
		horLayout = QVBoxLayout()
		horWidget.setLayout(horLayout)
		mainLayout.addWidget(horWidget)

		

		#Buttons for the left part of the layout

		button = QPushButton("Toggle laser")
		gridLayout.addWidget(button,0,0)

		button = QPushButton("Bluetooth Connect")
		gridLayout.addWidget(button,0,2)

		#Boxes for displaying last measured distance and angle. Blocked, will be updated by later functions

		self.boxDistance = QLineEdit("Last distance:")
		self.boxDistance.setReadOnly(True)
		gridLayout.addWidget(self.boxDistance,2,0)

		self.boxAngle = QLineEdit("Angle: 34.3")
		self.boxAngle.setReadOnly(True)
		gridLayout.addWidget(self.boxAngle,2,2)

		self.boxPointToPoint = QLineEdit("P2P: 13.4m")
		self.boxPointToPoint.setReadOnly(True)
		gridLayout.addWidget(self.boxPointToPoint,2,1)

		#Push Buttons For moving right, left and taking measurement

		buttonLeft = QPushButton("<<<")
		gridLayout.addWidget(buttonLeft,3,0)


		buttonMeasure = QPushButton("Measure")
		gridLayout.addWidget(buttonMeasure,3,1)


		buttonRight = QPushButton(">>>")
		gridLayout.addWidget(buttonRight,3,2)


		#Buttons for setting angle to relative 0 and displaying distance p2p

		buttonSetRelativeZero = QPushButton("Set angle 0")
		gridLayout.addWidget(buttonSetRelativeZero,4,0)

		buttonPointToPoint = QPushButton("Point to point")
		gridLayout.addWidget(buttonPointToPoint,4,2)





		#Set up threads. Initialise objects and move them to threads
		self.controlThread = QThread()
		self.commsThread = QThread()

		controlThreadObject = Control()
		commsThreadObject = Comms()

		controlThreadObject.moveToThread(self.controlThread)
		commsThreadObject.moveToThread(self.commsThread)
		
		self.controlThread.start()
		self.commsThread.start()


		self.show()




	def __del__(self):
		#Destructor. Initialise closing the thread, wait for it to finish, continue
		self.controlThread.quit()
		self.controlThread.wait()
		self.commsThread.quit()
		self.controlThread.wait()



	def buttonMeasureClicked():
		#A slot which handles Measure button click 
		return

	def buttonSetRelativeAngleToZeroClicked():
		#Slot which set  relative angle to zero degrees. Useful for calibration
		return


	def buttonMoveRightPressed():
		#Slot  
		return

	def buttonMoveRightReleased():
		#Slot
		return

	def buttonMoveLeftPressed():
		#Slot  
		return

	def buttonMoveLeftReleased():
		#Slot
		return

	def getDistanceBetweenTwoLastPointsPressed():
		#Slot. Uses two last measurements and returns distance between these points  
		return





