try: import PyQt5
except ModuleNotFoundError: __import__("os").system("pip3 install PyQt5")

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class Window(QMainWindow):
	def __init__(self):
		super(Window, self).__init__()
		self.resize(400, 400)
		self.setWindowTitle("Light Cycle")
		self.setStyleSheet("background-color: white")
		self.rectangle = QWidget(self)
		self.rectangle.resize(50, 80)
		self.rectangle.setStyleSheet("background-color: green")


application, window = QApplication([]), Window()
application.exec_()
