from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread, qDebug, pyqtSignal
from control import *
from PyQt5 import QtGui
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
		self.updateDisplays() #delete later

		self.displayPikaPika()
		
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

		self.setUpCentralWidget()
		self.setUpMenuWidget()
		self.setUpStackedLayoutWidget()
		self.setUpControlGridWidget()
		self.setUpImagesWidget()
		self.setUpDataDisplayWidget()
		self.addMenuButtons()
		self.addButtonsToControlGrid()
		self.addDisplaysToControlGrid()
		self.initialiseVariablesToZero()


		return
	def setUpMenuWidget(self):
		menuWidget = QWidget()
		menuWidget.setMinimumSize(800,20)
		self.menuLayout = QHBoxLayout()
		menuWidget.setLayout(self.menuLayout)
		self.mainLayout.addWidget(menuWidget)
		return

		
	def setUpStackedLayoutWidget(self):
		stackedWidget = QWidget()
		stackedWidget.setMinimumSize(800,380)
		self.stackedLayout = QStackedLayout()
		stackedWidget.setLayout(self.stackedLayout)
		self.mainLayout.addWidget(stackedWidget)

		return

	def setUpCentralWidget(self):
		mainWidget = QWidget()
		self.mainLayout = QVBoxLayout()
		mainWidget.setLayout(self.mainLayout)
		self.setCentralWidget(mainWidget)
		return

	def setUpControlGridWidget(self):
		self.controlWidget = QWidget()
		self.controlWidget.setMinimumSize(800,380)
		self.controlLayout = QGridLayout()
		self.controlWidget.setLayout(self.controlLayout)
		self.stackedLayout.addWidget(self.controlWidget)
		return

	def setUpImagesWidget(self):
		self.imagesWidget = QWidget()
		self.imagesWidget.setMinimumSize(800,380)
		self.imagesLayout = QHBoxLayout()
		self.imagesWidget.setLayout(self.imagesLayout)
		self.stackedLayout.addWidget(self.imagesWidget)

	def setUpDataDisplayWidget(self):
		self.dataDisplayWidget = QWidget()
		self.dataDisplayWidget.setMinimumSize(800,380)
		self.dataDisplayLayout = QVBoxLayout()
		self.dataDisplayWidget.setLayout(self.dataDisplayLayout)
		self.stackedLayout.addWidget(self.dataDisplayWidget)
		return


	def addMenuButtons(self):
		buttonControl = QPushButton("Control Panel")
		buttonControl.setFixedHeight(40)
		buttonControl.clicked.connect(self.switchStackedLayoutWidget(self.controlWidget))
		self.menuLayout.addWidget(buttonControl)

		buttonDisplay = QPushButton("Display data")
		buttonDisplay.setFixedHeight(40)
		buttonDisplay.clicked.connect(self.switchStackedLayoutWidget(self.dataDisplayWidget))
		self.menuLayout.addWidget(buttonDisplay)

		buttonImages = QPushButton("Maps and images")
		buttonImages.setFixedHeight(40)
		buttonImages.clicked.connect(self.switchStackedLayoutWidget(self.imagesWidget))
		self.menuLayout.addWidget(buttonImages)

		return

	def switchStackedLayoutWidget(self, widget):
		#this is an interesting concept. I couldn't pass a widget directly to the setCurrentWidget
		#I had to use something called function factory
		#https://stackoverflow.com/questions/6784084/how-to-pass-arguments-to-functions-by-the-click-of-button-in-pyqt
		#More information on stack 
		def functionFactory():
			self.stackedLayout.setCurrentWidget(widget)
		return functionFactory

	def initialiseVariablesToZero(self):
		self.lastDistance = 0
		self.lastAngle = 0
		self.formerDistance = 0
		self.formerAngle = 0
		self.lastWidth = 0
		return

	def updateDisplays(self):
		self.boxDistanceLast.setText("Last distance: " + str(self.lastDistance) )
		self.boxAngleLast.setText("Last angle: " + str(self.lastAngle))
		self.boxDistanceFormer.setText("Former distance: " + str(self.formerDistance))
		self.boxAngleFormer.setText("Former angle: " + str(self.formerAngle))
		self.boxWidth.setText("Last width: " + str(self.lastWidth))
		return


	def addDisplaysToControlGrid(self):
		self.boxDistanceLast = QLineEdit()
		self.boxDistanceLast.setFixedHeight(40)
		self.boxDistanceLast.setReadOnly(True)
		self.controlLayout.addWidget(self.boxDistanceLast,2,0)

		self.boxAngleLast = QLineEdit()
		self.boxAngleLast.setFixedHeight(40)
		self.boxAngleLast.setReadOnly(True)
		self.controlLayout.addWidget(self.boxAngleLast,2,1)

		self.boxDistanceFormer = QLineEdit()
		self.boxDistanceFormer.setFixedHeight(40)
		self.boxDistanceFormer.setReadOnly(True)
		self.controlLayout.addWidget(self.boxDistanceFormer,3,0)

		self.boxAngleFormer = QLineEdit()
		self.boxAngleFormer.setFixedHeight(40)
		self.boxAngleFormer.setReadOnly(True)
		self.controlLayout.addWidget(self.boxAngleFormer,3,1)

		self.boxWidth = QLineEdit()
		self.boxWidth.setFixedHeight(40)
		self.boxWidth.setReadOnly(True)
		self.controlLayout.addWidget(self.boxWidth,2,2)

		return 

	def addButtonsToControlGrid(self):
		buttonToggleLaser = QPushButton("Toggle laser")
		buttonToggleLaser.setFixedHeight(40)
		buttonToggleLaser.clicked.connect(self.buttonToggleLaserClicked)
		self.controlLayout.addWidget(buttonToggleLaser,0,0)

		buttonBluetoothConnect = QPushButton("Bluetooth Connect")
		buttonBluetoothConnect.setFixedHeight(40)
		buttonBluetoothConnect.clicked.connect(self.buttonBluetoothConnectClicked)
		self.controlLayout.addWidget(buttonBluetoothConnect,0,2)

		#Boxes for displaying last measured distance and angle. Blocked, will be updated by later functions
		

		#Push Buttons For moving right, left and taking measurement

		buttonLeft = QPushButton("<<<")
		buttonLeft.pressed.connect(self.buttonMoveLeftPressed)
		buttonLeft.released.connect(self.buttonMoveLeftReleased)
		buttonLeft.setFixedHeight(60)
		self.controlLayout.addWidget(buttonLeft,6,0)


		buttonMeasure = QPushButton("Measure")
		buttonMeasure.clicked.connect(self.buttonMeasureClicked)
		buttonMeasure.setFixedHeight(60)
		self.controlLayout.addWidget(buttonMeasure,6,1)


		buttonRight = QPushButton(">>>")
		buttonRight.pressed.connect(self.buttonMoveRightPressed)
		buttonRight.released.connect(self.buttonMoveRightReleased)
		buttonRight.setFixedHeight(60)
		self.controlLayout.addWidget(buttonRight,6,2)


		#Buttons for setting angle to relative 0 and displaying distance p2p

		buttonSetRelativeZero = QPushButton("Set angle 0")
		buttonSetRelativeZero.setFixedHeight(40)
		buttonSetRelativeZero.clicked.connect(self.buttonSetRelativeAngleToZeroClicked)
		self.controlLayout.addWidget(buttonSetRelativeZero,8,0)

		buttonWidth = QPushButton("Calculate width")
		buttonWidth.setFixedHeight(40)
		buttonWidth.clicked.connect(self.buttonGetWidthPressed)
		self.controlLayout.addWidget(buttonWidth,8,2)

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
		self.moveLeftStopSignal.emit()
		return

	def buttonGetWidthPressed(self):
		#Slot. Uses two last measurements and returns distance between these points  
		self.calculateWidthSignal.emit()
		return

	def buttonBluetoothConnectClicked(self):
		#Slot
		return

	def displayPikaPika(self):
		pika = QLabel(self)
		pix = QtGui.QPixmap("pika.png")
		pix = pix.scaled(800,380)
		pika.setPixmap(pix)
		self.imagesLayout.addWidget(pika)


		pika.show()



		return 
