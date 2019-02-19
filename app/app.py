from gui import MainWindow
from PyQt5.QtWidgets import *
import sys

if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = MainWindow()
	sys.exit(app.exec_())