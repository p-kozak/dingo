from PyQt5.QtCore import QObject

class Comms(QObject):
	def __init__(self, parent = None):
		QObject.__init__(self)

	