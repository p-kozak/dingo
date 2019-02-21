from PyQt5.QtCore import QObject, qDebug

class Control(QObject):
	#Signals going to gui(engine)


	def __init__(self, parent = None):
		QObject.__init__(self)

		return 

	def defineSignals(self):
		
		return

	#These are slots which receive from engine
	def toggleLaser(self):		
		return 

	def moveRightStart(self):
		return

	def moveRightStop(self):
		return

	def moveLeftStart(self):
		return

	def moveLeftStop(self):
		return

	def measureDistance(self):
		return

	def setAngleToZero(self):
		return

	def calculateWidth(self):
		return 

