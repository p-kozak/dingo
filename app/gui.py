from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread, qDebug, pyqtSignal, Qt
from control import *
from PyQt5 import QtGui
from PyQt5.QtGui import QPalette, QImage
from comms import Comms
from mapswidget import MapsDisplay
from settingswidget import SettingsWidget
from datadisplay import DataDisplay
from dataprocessing import Map, Point
from mapscontrolwidget import MapsControl
import os, signal









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
	sendSpeedSignal = pyqtSignal(int)
	connectBluetoothSignal = pyqtSignal()
	getMapSignal = pyqtSignal()


	def __init__(self, parent = None):
		QMainWindow.__init__(self)
		#self.setStyleSheet("background-color: black;")
		#self.setStyleSheet(".QPushButton { background-color: black}")
		self.setAutoFillBackground(True)

		#Set the properties of the window
		self.setMinimumSize(800,480)
		self.setWindowTitle("Dingo is amazing")
		
		#initialise widgets and threads
		self.displayWidgets()
		self.setUpThreads()
		self.defineSignals()

		self.updateDisplays() #delete later
		self.updateLaserColour()

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
		self.setUpSettingsWidget()
		self.setUpImagesWidget()
		self.setUpDataDisplayWidget()
		self.setUpMapsControlWidget()
		self.addMenuButtons()
		self.addButtonsToControlGrid()
		self.addDisplaysToControlGrid()
		self.initialiseVariablesToZero()
		self.addMotorSpeedControls()
		self.addWarningDisplay()
		self.initialiseSpeedVariable()
		#self.addSliderToControlGrid()


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
		self.imagesWidget = MapsDisplay()
		# self.imagesWidget.setMinimumSize(800,380)
		# self.imagesLayout = QHBoxLayout()
		# self.imagesWidget.setLayout(self.imagesLayout)
		self.stackedLayout.addWidget(self.imagesWidget)

	def setUpDataDisplayWidget(self):
		self.dataDisplayWidget = DataDisplay()
		# self.dataDisplayWidget.setMinimumSize(800,380)
		# self.dataDisplayLayout = QVBoxLayout()
		# self.dataDisplayWidget.setLayout(self.dataDisplayLayout)
		self.stackedLayout.addWidget(self.dataDisplayWidget)
		return

	def setUpMapsControlWidget(self):
		self.mapsControlWidget = MapsControl()
		self.stackedLayout.addWidget(self.mapsControlWidget)

	def setUpSettingsWidget(self):
		self.settingsWidget = SettingsWidget()
		self.stackedLayout.addWidget(self.settingsWidget)


	def addMenuButtons(self):
		buttonControl = QPushButton("Control Panel")
		buttonControl.setFixedHeight(40)
		buttonControl.clicked.connect(self.switchStackedLayoutWidget(self.controlWidget))
		self.menuLayout.addWidget(buttonControl)

		buttonDisplay = QPushButton("Display data")
		buttonDisplay.setFixedHeight(40)
		buttonDisplay.clicked.connect(self.switchStackedLayoutWidget(self.dataDisplayWidget))
		self.menuLayout.addWidget(buttonDisplay)

		buttonMaps = QPushButton("Maps control")
		buttonMaps.setFixedHeight(40)
		buttonMaps.clicked.connect(self.switchStackedLayoutWidget(self.mapsControlWidget))
		self.menuLayout.addWidget(buttonMaps)

		buttonImages = QPushButton("Maps")
		buttonImages.setFixedHeight(40)
		buttonImages.clicked.connect(self.switchStackedLayoutWidget(self.imagesWidget))
		self.menuLayout.addWidget(buttonImages)

		buttonSettings = QPushButton("Settings")
		buttonSettings.setFixedHeight(40)
		buttonSettings.clicked.connect(self.switchStackedLayoutWidget(self.settingsWidget))
		self.menuLayout.addWidget(buttonSettings)


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
		self.lastWidthDistance = 0
		self.laserOn = False
		return

	def initialiseSpeedVariable(self):
		self.speed = 5
		return

	def updateDisplays(self):
		self.boxDistanceLast.setText("Last distance: " + str(self.lastDistance) + "mm")
		self.boxAngleLast.setText("Last angle: " + str(self.lastAngle))
		self.boxDistanceFormer.setText("Former distance: " + str(self.formerDistance) + "mm")
		self.boxAngleFormer.setText("Former angle: " + str(self.formerAngle))
		self.boxWidth.setText("Last width: " + str(self.lastWidth) + "mm")
		self.boxSpeed.setText("Motor speed: " + str(self.speed))
		self.boxWidthDistance.setText("Shortest distance: " + str(self.lastWidthDistance) + "mm")

		if self.lastDistance != 0 and self.lastDistance < 1000:
			self.boxWarning.setText("WARNING. Distance under 1m. It can be inaccurate")
			self.boxWarning.setStyleSheet("background-color: red")
		elif self.lastDistance != 0 and self.lastDistance > 1000:
			self.boxWarning.setText("Measurement OK")
			self.boxWarning.setStyleSheet("background-color: green")
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

		self.boxSpeed = QLineEdit()
		self.boxSpeed.setFixedHeight(40)
		self.boxSpeed.setReadOnly(True)
		self.controlLayout.addWidget(self.boxSpeed,5,1)

		self.boxWidthDistance = QLineEdit()
		self.boxWidthDistance.setFixedHeight(40)
		self.boxWidthDistance.setReadOnly(True)
		self.controlLayout.addWidget(self.boxWidthDistance,3,2)

		return 

	def addSliderToControlGrid(self):
		self.slider = QSlider()
		self.slider.setRange(1,10)
		self.slider.setTickPosition(1)
		self.slider.setTickInterval(10)
		self.slider.setSingleStep(1)
		self.slider.setOrientation(1)
		self.controlLayout.addWidget(self.slider,5,0,1,2)
		return

	def addButtonsToControlGrid(self):
		self.buttonToggleLaser = QPushButton("Toggle laser: OFF")
		#buttonToggleLaser.setStyleSheet("background-color: white")
		self.buttonToggleLaser.setFixedHeight(50)
		self.buttonToggleLaser.setStyleSheet("background-color: green")
		self.buttonToggleLaser.clicked.connect(self.buttonToggleLaserClicked)
		self.controlLayout.addWidget(self.buttonToggleLaser,0,0)

		self.buttonBluetoothConnect = QPushButton("Bluetooth Connect")
		self.buttonBluetoothConnect.setFixedHeight(50)
		self.buttonBluetoothConnect.clicked.connect(self.buttonBluetoothConnectClicked)
		self.controlLayout.addWidget(self.buttonBluetoothConnect,0,2)

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

		# Moved to maps control tab
		buttonScan = QPushButton("Map the room")
		buttonScan.setFixedHeight(40)
		buttonScan.clicked.connect(self.buttonScanRoomClicked)
		# self.controlLayout.addWidget(buttonScan,8,2)

		return 

	def addButtonUpdate(self):
		buttonUpdate = QPushButton("UPdate")
		buttonUpdate.setFixedHeight(40)
		buttonUpdate.clicked.connect(self.updateFirmware)
		self.controlLayout.addWidget(buttonUpdate,3,2)


	def addMotorSpeedControls(self):
		buttonDecreaseSpeed = QPushButton("---")
		buttonDecreaseSpeed.setFixedHeight(40)
		buttonDecreaseSpeed.clicked.connect(self.buttonDecreaseSpeedClicked)
		self.controlLayout.addWidget(buttonDecreaseSpeed,5,0)


		buttonIncreaseSpeed = QPushButton("+++")
		buttonIncreaseSpeed.setFixedHeight(40)
		buttonIncreaseSpeed.clicked.connect(self.buttonIncreaseSpeedClicked)
		self.controlLayout.addWidget(buttonIncreaseSpeed,5,2)

		return

	def defineSignals(self):
		#gui -> control
		self.toggleLaserSignal.connect(self.controlThreadObject.toggleLaser)
		self.moveRightStartSignal.connect(self.controlThreadObject.moveRightStart)
		self.moveRightStopSignal.connect(self.controlThreadObject.moveRightStop)
		self.moveLeftStartSignal.connect(self.controlThreadObject.moveLeftStart)
		self.moveLeftStopSignal.connect(self.controlThreadObject.moveLeftStop)
		self.measureDistanceSignal.connect(self.controlThreadObject.measureDistance)
		self.setAngleToZeroSignal.connect(self.controlThreadObject.setAngleToZero)
		self.calculateWidthSignal.connect(self.controlThreadObject.calculateWidth)
		self.sendSpeedSignal.connect(self.controlThreadObject.receiveSpeedValue)

		#maps control -> gui
		self.mapsControlWidget.getMapSignal.connect(self.controlThreadObject.getMap)
		self.mapsControlWidget.turnOffLaserSignal.connect(self.turnOffLaser)

		#maps -> maps control
		self.imagesWidget.mapAddedSignal.connect(self.mapsControlWidget.indicatorFinishMeasurment)

		#control -> gui
		self.controlThreadObject.sendMapSignal.connect(self.receiveMap)
		self.controlThreadObject.sendPointSignal.connect(self.receivePoint)

		#gui -> comms
		self.connectBluetoothSignal.connect(self.commsThreadObject.main)

		#comms -> gui

		self.commsThreadObject.calculateWidthSignal.connect(self.buttonGetWidthPressed)
		self.commsThreadObject.toggleLaserSignal.connect(self.buttonToggleLaserClicked)
		self.commsThreadObject.getMapSignal.connect(self.controlThreadObject.getMap)
		self.commsThreadObject.measureSignal.connect(self.buttonMeasureClicked)
		self.commsThreadObject.setAngleZeroSignal.connect(self.buttonSetRelativeAngleToZeroClicked)
		self.commsThreadObject.bluetoothReadySignal.connect(self.bluetoothConnected)

		return




	def turnOffLaser(self):
		self.laserOn = False
		self.updateLaserColour()
		return

	def bluetoothConnected(self):
		self.buttonBluetoothConnect.setText("Bluetooth ready")
		return

	def buttonToggleLaserClicked(self):
		self.laserOn = not self.laserOn
		self.toggleLaserSignal.emit()
		self.updateLaserColour()

		return

	def updateLaserColour(self):
		if self.laserOn is True:
			self.buttonToggleLaser.setStyleSheet("background-color: red")
			self.buttonToggleLaser.setText("Toggle laser: ON")
		elif self.laserOn is not True:
			self.buttonToggleLaser.setStyleSheet("background-color: green")
			self.buttonToggleLaser.setText("Toggle laser: OFF")



	def buttonMeasureClicked(self):
		#A slot which handles Measure button click 
		self.measureDistanceSignal.emit()
		# point = Point()
		# point.value = 6
		# point.angle = 56
		# point.error = 43
		# self.dataDisplayWidget.addPointToDisplay(point)
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
	def buttonIncreaseSpeedClicked(self):
		if self.speed >= 10:
			return
		else:
			self.speed +=1
			self.sendSpeedSignal.emit(self.speed)
			self.updateDisplays()
		return


	def buttonDecreaseSpeedClicked(self):
		if self.speed <= 1:
			return
		else:
			self.speed -=1
			self.sendSpeedSignal.emit(self.speed)
			self.updateDisplays()
		return

	def buttonGetWidthPressed(self):
		#Slot. Uses two last measurements and returns distance between these points  
		self.calculateWidthSignal.emit()
		# point = Point()
		# point.value = 6324
		# point.objectType = "width"
		# point.angle = 99999
		# point.error = 43
		# self.dataDisplayWidget.addMeasurementToDisplay(point)
		return

	def buttonBluetoothConnectClicked(self):
		#Slot
		self.connectBluetoothSignal.emit()
		return

	def displayPikaPika(self):
		pika = QLabel(self)
		pix = QtGui.QPixmap("pika.png")
		pix = pix.scaled(800,380)
		pika.setPixmap(pix)
		self.imagesLayout.addWidget(pika)


		pika.show()

		return 

	def buttonScanRoomClicked(self):
		self.getMapSignal.emit()

		return

	def sendMarkNixon(self):
		img = QImage("nix.png")
		mp = Map()
		mp.mapImage = img
		self.imagesWidget.addNewMapPair(mp)
		return

	def receivePoint(self, point):
		point.value = round(point.value,2)
		point.angle = round(point.angle,2)
		point.error = round(point.error,2)

		if point.objectType == "point":
			self.updateLastDistance(point)
			self.dataDisplayWidget.addMeasurementToDisplay(point)
		elif point.objectType == "width":			
			self.commsThreadObject.response = "msg:" + str(point.value) + "," + str(point.angle)
			self.updateWidht(point)
			self.dataDisplayWidget.addMeasurementToDisplay(point)
		return


	def receiveMap(self, imageMap):
		self.imagesWidget.addNewMapPair(imageMap)

		return 

	def updateLastDistance(self, point):
		#Move last to former
		self.formerDistance = self.lastDistance
		self.formerAngle = self.lastAngle

		self.lastDistance = point.value
		self.lastAngle = point.angle

		self.updateDisplays()

		return

	def updateWidht(self, point):
		self.lastWidth = point.value
		self.lastWidthDistance = point.angle
		self.updateDisplays()
		return

	def updateFirmware(self):
		pid = os.getpid()
		os.system("sudo python3 updater.py")
		os.kill(pid, signal.SIGKILL)

		return

	def addWarningDisplay(self):
		self.boxWarning = QTextEdit("Measurements under 1m are likely to be inaccurate")
		self.boxWarning.setStyleSheet("background-color: white")
		self.boxWarning.setAlignment(Qt.AlignCenter)
		self.boxWarning.setReadOnly(True)
		self.boxWarning.setFixedHeight(50)
		self.controlLayout.addWidget(self.boxWarning, 0, 1)





