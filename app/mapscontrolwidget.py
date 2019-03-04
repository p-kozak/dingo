from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import pyqtSignal


class MapsControl(QWidget):
	getMapSignal = pyqtSignal(int, int, int)

	def __init__(self):
		QWidget.__init__(self)
		self.initialiseGridLayout()
		self.initialiseDefaultValues()
		self.addAngleButtons()
		self.addDisplays()
		self.addResolutionButtons()
		self.addScanButtons()
		self.updateDisplays()

		


	def initialiseDefaultValues(self):
		self.leftAngle = -45
		self.rightAngle = 45
		self.resolution = 5
		return


	def initialiseGridLayout(self):
		self.gridLayout = QGridLayout()
		self.setLayout(self.gridLayout)
		return

	def addAngleButtons(self):
		buttonLeftIncrease = QPushButton("+++")
		buttonLeftIncrease.setFixedHeight(60)
		buttonLeftIncrease.clicked.connect(self.buttonAngleLeftIncreaseClicked)
		self.gridLayout.addWidget(buttonLeftIncrease,0,0)

		buttonLeftDecrease = QPushButton("---")
		buttonLeftDecrease.setFixedHeight(60)
		buttonLeftDecrease.clicked.connect(self.buttonAngleLeftDecreaseClicked)
		self.gridLayout.addWidget(buttonLeftDecrease,2,0)

		buttonRightIncrease = QPushButton("+++")
		buttonRightIncrease.setFixedHeight(60)
		buttonRightIncrease.clicked.connect(self.buttonAngleRightIncreaseClicked)
		self.gridLayout.addWidget(buttonRightIncrease,0,2)

		buttonRightDecrease = QPushButton("---")
		buttonRightDecrease.setFixedHeight(60)
		buttonRightDecrease.clicked.connect(self.buttonAngleRightDecreaseClicked)
		self.gridLayout.addWidget(buttonRightDecrease,2,2)

	def addDisplays(self):
		self.leftAngleDisplay = QLineEdit()
		self.leftAngleDisplay.setFixedHeight(60)
		self.leftAngleDisplay.setReadOnly(True)
		self.gridLayout.addWidget(self.leftAngleDisplay,1,0)

		self.rightAngleDisplay = QLineEdit()
		self.rightAngleDisplay.setFixedHeight(60)
		self.rightAngleDisplay.setReadOnly(True)
		self.gridLayout.addWidget(self.rightAngleDisplay,1,2)

		self.resolutionDisplay = QLineEdit()
		self.resolutionDisplay.setFixedHeight(60)
		self.resolutionDisplay.setReadOnly(True)
		self.gridLayout.addWidget(self.resolutionDisplay,4,1)

	def updateDisplays(self):
		self.leftAngleDisplay.setText("Left angle: " + str(self.leftAngle))
		self.rightAngleDisplay.setText("Right angle: " + str(self.rightAngle))
		self.resolutionDisplay.setText("Resolution: " + str(self.resolution))


	def buttonAngleLeftIncreaseClicked(self):
		if self.leftAngle < -5:
			self.leftAngle += 5
		if self.leftAngle > -5:
			self.leftAngle = -5
		self.updateDisplays()
		return

	def buttonAngleLeftDecreaseClicked(self):
		if self.leftAngle > -180:
			self.leftAngle -= 5
		if self.leftAngle < -180:
			self.leftAngle = -180
		self.updateDisplays()
		return

	def buttonAngleRightIncreaseClicked(self):
		if self.rightAngle < 180:
			self.rightAngle += 5
		if self.rightAngle > 180:
			self.rightAngle = 180
		self.updateDisplays()
		return

	def buttonAngleRightDecreaseClicked(self):
		if self.rightAngle > 5:
			self.rightAngle -= 5
		if self.rightAngle < 5:
			self.rightAngle = 5
		self.updateDisplays()
		return


	def addResolutionButtons(self):
		buttonResolutionIncrease = QPushButton("+++")
		buttonResolutionIncrease.setFixedHeight(60)
		buttonResolutionIncrease.clicked.connect(self.increaseResolution)
		self.gridLayout.addWidget(buttonResolutionIncrease,4,2)

		buttonResolutionDecrease = QPushButton("---")
		buttonResolutionDecrease.setFixedHeight(60)
		buttonResolutionDecrease.clicked.connect(self.decreaseResolution)
		self.gridLayout.addWidget(buttonResolutionDecrease,4,0)
		return 


	def decreaseResolution(self):
		self.resolution -= 1
		if self.resolution <=1:
			self.resolution = 1
		self.updateDisplays()
		return

	def increaseResolution(self):
		self.resolution += 1
		if self.resolution >= 10:
			self.resolution = 10
		self.updateDisplays()
		return

	def addScanButtons(self):
		buttonPartial = QPushButton("Partial scan")
		buttonPartial.setFixedHeight(60)
		buttonPartial.clicked.connect(self.emitGetPartialScan)
		self.gridLayout.addWidget(buttonPartial, 1,1)

		buttonFull = QPushButton("Full scan")
		buttonFull.setFixedHeight(60)
		buttonFull.clicked.connect(self.emitGetFullScan)
		self.gridLayout.addWidget(buttonFull, 2,1)



	def emitGetPartialScan(self):
		self.getMapSignal.emit(self.leftAngle, self.rightAngle, self.resolution)
		return

	def emitGetFullScan(self):
		self.getMapSignal.emit(-180, 180, self.resolution)
		return





