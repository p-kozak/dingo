from PyQt5.QtWidgets import *
from functools import partial
from PyQt5.QtGui import *


class MapsDisplay(QWidget):
	def __init__(self):
		self.count = 0
		self.listOfImages = []
		self.listOfIndices = []
		QWidget.__init__(self)
		self.layout = QHBoxLayout()
		self.setLayout(self.layout)
		self.inistialiseScrollArea()
		self.addWidgetToScroll()
		self.initialiseStackedLayout()
	

		

	def inistialiseScrollArea(self):
		self.scrollArea = QScrollArea()
		self.scrollArea.setFixedWidth(85)
		self.scrollArea.setWidgetResizable(True)
		self.layout.addWidget(self.scrollArea)
		return

	def addWidgetToScroll(self):
		stripWidget = QWidget()
		self.stripLayout = QVBoxLayout()
		stripWidget.setLayout(self.stripLayout)
		self.scrollArea.setWidget(stripWidget)
		return

	def addTemp(self):
		widget = QWidget()
		templayout = QVBoxLayout()
		widget.setLayout(templayout)
		templayout.addWidget(QPushButton("gowno"))
		self.layout.addWidget(widget)
		return

	def initialiseStackedLayout(self):
		stackedWidget = QWidget()
		self.stackedLayout = QStackedLayout()
		stackedWidget.setLayout(self.stackedLayout)
		self.layout.addWidget(stackedWidget)
		return

	def addNewMapPair(self, image):
		self.addNewImage(image.imageMap)
		self.addNewButton()
		return

	def addNewButton(self):
		index = self.count 
		button = QPushButton(str(index+1))
		button.setFixedSize(50,50)
		button.clicked.connect(partial(self.switchStackedImages, index))
		self.stripLayout.addWidget(button)
		self.count += 1
		return

	def addNewImage(self, imageMap):
		index = self.count
		image = imageMap

		label = QLabel(self)
		pix = QPixmap()
		pix = pix.fromImage(image)
		pix = pix.scaled(700,360)
		label.setPixmap(pix)
		#self.imagesLayout.addWidget(pika)


		self.listOfImages.append(label)
		self.listOfIndices.append(index)
		self.stackedLayout.addWidget(self.listOfImages[index])
		return
		

	def switchStackedImages(self, index):
		self.stackedLayout.setCurrentWidget(self.listOfImages[index])
		return






