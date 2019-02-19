from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread
from control import Control
from comms import Comms


class MainWindow(QMainWindow):
	def __init__(self, parent = None):
		QMainWindow.__init__(self)
		self.setWindowTitle("Dingo is amazing")
		
		#test code just to put something on the grid
		widget = QWidget()
		layout = QGridLayout()
		widget.setLayout(layout)
		self.setCentralWidget(widget)
		button = QPushButton("dupa")
		layout.addWidget(button, 0,0)


		#set up threads. set up objects and move them to threads
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
		#initialise closing the thread, wait for it to finish
		self.controlThread.quit()
		self.controlThread.wait()
		self.commsThread.quit()
		self.controlThread.wait()






