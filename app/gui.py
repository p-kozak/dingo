from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread, qDebug, pyqtSignal
from control import Control
from comms import Comms




class MainWindow(QMainWindow):

	#Signals which go to control. They have to be declared here due to limitations of the PyQt5
	#https://stackoverflow.com/questions/2970312/pyqt4-qtcore-pyqtsignal-object-has-no-attribute-connect
	#well explained in the link above
	toggleLaserSignal = pyqtSignal()
	moveRightStartSignal = pyqtSignal()
	moveRightStopSignal = pyqtSignal()
	moveLeftStartSignal = pyqtSignal()
	moveLeftStopSignal = pyqtSignal()
	measureDistanceSignal = pyqtSignal()
	setAngleToZeroSignal = pyqtSignal()
	calculateWidthSignal = pyqtSignal()


	def __init__(self, parent = None):
		QMainWindow.__init__(self)
		#Set the properties of the window
		self.setMinimumSize(800,480)
		self.setWindowTitle("Dingo is amazing")
		
		#initialise widgets and threads
		self.displayWidgets()
		self.setUpThreads()
		self.defineSignals()
		
		self.show()




	def __del__(self):
		#Destructor. Initialise closing the thread, wait for it to finish, continue
		self.controlThread.quit()
		self.controlThread.wait()
		self.commsThread.quit()
		self.controlThread.wait()


	def setUpThreads(self):
		#Set up threads. Initialise objects and move them to threads
		self.controlThread = QThread()
		self.commsThread = QThread()

		self.controlThreadObject = Control()
		self.commsThreadObject = Comms()

		self.controlThreadObject.moveToThread(self.controlThread)
		self.commsThreadObject.moveToThread(self.commsThread)
		
		self.controlThread.start()
		self.commsThread.start()

		return 



	def displayWidgets(self):

		mainWidget = QWidget()
		mainLayout = QHBoxLayout()
		mainWidget.setLayout(mainLayout)
		self.setCentralWidget(mainWidget)

		#Layout and widget for the left part of the GUI - buttons
		gridWidget = QWidget()
		gridWidget.setMinimumSize(280,480)
		self.controlLayout = QGridLayout()
		gridWidget.setLayout(self.controlLayout)
		mainLayout.addWidget(gridWidget)



		#Prototype layout and widget for the right part of the GUI- display
		horWidget = QWidget()
		horWidget.setMinimumSize(520,480)
		self.displayLayout = QVBoxLayout()
		horWidget.setLayout(self.displayLayout)
		mainLayout.addWidget(horWidget)

		

		#Buttons for the left part of the layout

		button = QPushButton("Toggle laser")
		button.clicked.connect(self.buttonToggleLaserClicked)
		self.controlLayout.addWidget(button,0,0)

		button = QPushButton("Bluetooth Connect")
		self.controlLayout.addWidget(button,0,2)

		#Boxes for displaying last measured distance and angle. Blocked, will be updated by later functions

		self.boxDistance = QLineEdit("Last distance: 4.2m")
		self.boxDistance.setReadOnly(True)
		self.controlLayout.addWidget(self.boxDistance,2,0)

		self.boxAngle = QLineEdit("Angle: 34.3")
		self.boxAngle.setReadOnly(True)
		self.controlLayout.addWidget(self.boxAngle,2,2)

		self.boxPointToPoint = QLineEdit("P2P: 13.4m")
		self.boxPointToPoint.setReadOnly(True)
		self.controlLayout.addWidget(self.boxPointToPoint,2,1)

		#Push Buttons For moving right, left and taking measurement

		buttonLeft = QPushButton("<<<")
		self.controlLayout.addWidget(buttonLeft,3,0)


		buttonMeasure = QPushButton("Measure")
		self.controlLayout.addWidget(buttonMeasure,3,1)


		buttonRight = QPushButton(">>>")
		self.controlLayout.addWidget(buttonRight,3,2)


		#Buttons for setting angle to relative 0 and displaying distance p2p

		buttonSetRelativeZero = QPushButton("Set angle 0")
		self.controlLayout.addWidget(buttonSetRelativeZero,4,0)

		buttonPointToPoint = QPushButton("Point to point")
		self.controlLayout.addWidget(buttonPointToPoint,4,2)

		return


	def defineSignals(self):
		self.toggleLaserSignal.connect(self.controlThreadObject.toggleLaser)
		self.moveRightStartSignal.connect(self.controlThreadObject.moveRightStart)
		self.moveRightStopSignal.connect(self.controlThreadObject.moveRightStop)
		self.moveLeftStartSignal.connect(self.controlThreadObject.moveLeftStart)
		self.moveLeftStopSignal.connect(self.controlThreadObject.moveLeftStop)
		self.measureDistanceSignal.connect(self.controlThreadObject.measureDistance)
		self.setAngleToZeroSignal.connect(self.controlThreadObject.setAngleToZero)
		self.calculateWidthSignal.connect(self.controlThreadObject.calculateWidth)
		return

	def buttonToggleLaserClicked(self):
		qDebug("dupa wojtka")
		self.toggleLaserSignal.emit()
	
		return 


	def buttonMeasureClicked(self):
		#A slot which handles Measure button click 
		self.measureDistanceSignal.emit()
		return

	def buttonSetRelativeAngleToZeroClicked(self):
		#Slot which set  relative angle to zero degrees. Useful for calibration
		self.setAngleToZeroSignal.emit()
		return

	def buttonMoveRightPressed(self):
		#Slot 
		self.moveRightStartSignal.emit()
		return

	def buttonMoveRightReleased(self):
		#Slot
		self.moveRightStopSignal.emit()
		return

	def buttonMoveLeftPressed(self):
		#Slot 
		self.moveLeftStartSignal.emit() 
		return

	def buttonMoveLeftReleased(self):
		#Slot
		selff.moveLeftStopSignal.emit()
		return

	def getWidthPressed(self):
		#Slot. Uses two last measurements and returns distance between these points  
		self.getWidthPressed.emit()
		return


