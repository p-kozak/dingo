from PyQt5.QtWidgets import *
import os, signal

class SettingsWidget(QWidget):
	def __init__(self):
		QWidget.__init__(self)
		self.initialiseLayout()
		self.setUpExitButton()
		self.setUpUpdateButton()

	def initialiseLayout(self):
		self.layout = QVBoxLayout()
		self.setLayout(self.layout)

	def setUpExitButton(self):
		exitButton = QPushButton("Exit")
		exitButton.setFixedHeight(100)
		exitButton.clicked.connect(self.killSelf)
		self.layout.addWidget(exitButton)

	def setUpUpdateButton(self):
		updateButton = QPushButton("Update firmware (WIFI connection required) \
			DON'T CLICK IN DEV STAGE PLZ, DOES GIT STASH"
			)
		updateButton.setFixedHeight(100)
		updateButton.clicked.connect(self.updateFirmware)
		self.layout.addWidget(updateButton) 

	def killSelf(self):
		pid = os.getpid()
		os.kill(pid, signal.SIGKILL)

	def updateFirmware(self):
		os.system("sudo python3 updater.py")
		self.killSelf()
		






