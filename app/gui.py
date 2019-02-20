from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread
from control import Control
from comms import Comms


class MainWindow(QMainWindow): 
	def __init__(self, parent = None):
		QMainWindow.__init__(self)
		#Set the properties of the window
		self.setMinimumSize(800,480)
		self.setWindowTitle("Dingo is amazing")
		
		#test code just to put something on the grid
		mainWidget = QWidget()
		mainLayout = QHBoxLayout()
		mainWidget.setLayout(mainLayout)
		self.setCentralWidget(mainWidget)

		#Layout and widget for the left part of the GUI - buttons
		gridWidget = QWidget()
		gridWidget.setMinimumSize(280,480)
		gridLayout = QGridLayout()
		gridWidget.setLayout(gridLayout)
		mainLayout.addWidget(gridWidget)



		#Prototype layout and widget for the right part of the GUI- display
		horWidget = QWidget()
		horWidget.setMinimumSize(520,480)
		horLayout = QVBoxLayout()
		horWidget.setLayout(horLayout)
		mainLayout.addWidget(horWidget)

		#Buttons for the left part of the layout

		button = QPushButton("Toggle laser")
		gridLayout.addWidget(button,0,0)

		button = QPushButton("Bluetooth Connect")
		gridLayout.addWidget(button,0,1)

		boxDistanceLabel = QLabel("Last distance:")
		gridLayout.addWidget(boxDistanceLabel,1,0)

		boxAngleLabel = QLabel("Current angle:")
		gridLayout.addWidget(boxAngleLabel,1,1)

		boxDistanceLabel = QLabel("Last distance:")
		gridLayout.addWidget(boxDistanceLabel,1,0)

		boxAngleLabel = QLabel("Current angle:")
		gridLayout.addWidget(boxAngleLabel,1,1)






		
		


		#Set up threads. Initialise objects and move them to threads
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
		#Destructor. Initialise closing the thread, wait for it to finish, continue
		self.controlThread.quit()
		self.controlThread.wait()
		self.commsThread.quit()
		self.controlThread.wait()



	def buttonMeasureClicked():
		#A slot which handles Measure button click 
		return

	def buttonSetRelativeAngleToZeroClicked():
		#Slot which set  relative angle to zero degrees. Useful for calibration
		return


	def buttonMoveRightPressed():
		#Slot  
		return

	def buttonMoveRightReleased():
		#Slot
		return

	def buttonMoveLeftPressed():
		#Slot  
		return

	def buttonMoveLeftReleased():
		#Slot
		return

	def getDistanceBetweenTwoLastPointsPressed():
		#Slot. Uses two last measurements and returns distance between these points  
		return





