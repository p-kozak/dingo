from PyQt5.QtWidgets import *
from functools import partial


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


	def addWidgetToScroll(self):
		stripWidget = QWidget()
		self.stripLayout = QVBoxLayout()
		stripWidget.setLayout(self.stripLayout)
		self.scrollArea.setWidget(stripWidget)

	def addTemp(self):
		widget = QWidget()
		templayout = QVBoxLayout()
		widget.setLayout(templayout)
		templayout.addWidget(QPushButton("gowno"))
		self.layout.addWidget(widget)

	def initialiseStackedLayout(self):
		stackedWidget = QWidget()
		self.stackedLayout = QStackedLayout()
		stackedWidget.setLayout(self.stackedLayout)
		self.layout.addWidget(stackedWidget)

	def addNewMapPair(self, map):
		self.addNewImage()
		self.addNewButton()



	def addNewButton(self):
		index = self.count 
		button = QPushButton(str(index))
		button.setFixedSize(50,50)
		button.clicked.connect(partial(self.switchStackedImages, index))
		self.stripLayout.addWidget(button)
		self.count += 1

	def addNewImage(self):
		index = self.count
		button = QPushButton(str(index))
		self.listOfImages.append(button)
		self.listOfIndices.append(index)
		self.stackedLayout.addWidget(self.listOfImages[index])
		




	def switchStackedImages(self, index):
		self.stackedLayout.setCurrentWidget(self.listOfImages[index])






