from PyQt5 import QtWidgets
import sys

def window():
    app = QtWidgets.QApplication(sys.argv)
    win = QtWidgets.QMainWindow()
    win.setGeometry(300,300,400 ,400)
    win.setWindowTitle("Hello World")
    win.show()
    sys.exit(app.exec_())
window()
