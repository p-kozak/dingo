from control import *
from PyQt5.QtWidgets import *


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
		self.spamButtons()
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
		for i in range(20):
			button = QPushButton(str(i))
			button.setFixedHeight(70)
			self.gridDataLayout.addWidget(button,i,0)

		return



