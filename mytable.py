from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys

class mytable(QWidget):
    def __init__ (self, parent = None):
        super(mytable, self).__init__(parent)
        self.textQVBoxLayout = QVBoxLayout()
        self.textUpQLabel    = QLabel()
        self.textDownQLabel  = QLabel()
        self.textQVBoxLayout.addWidget(self.textUpQLabel)
        self.textQVBoxLayout.addWidget(self.textDownQLabel)
  
        
    def setTextUp (self, text):
        self.textUpQLabel.setText(text)

    def setTextDown (self, text):
        self.textDownQLabel.setText(text)

    '''    
    def add_new_entry(self):
        pass
    def table(self):
        self.setItem(0,0,QTableWidgetItem(""))
        self.setItem(0,1,QTableWidgetItem(""))
        self.setItem(0,2,QTableWidgetItem(""))
        self.setItem(0,3, QTableWidgetItem(""))
        self.setItem(0,4, QTableWidgetItem(""))
        self.setItem(0, 5, QTableWidgetItem(""))

        self.setHorizontalHeaderLabels(["1", "2", "3", "4", "5","6"])
        self.setVerticalHeaderLabels(["1", "2"])

        lbp = QLabel()
        lbp.setPixmap(QPixmap("youPicture.png"))
        self.setCellWidget(1,1,lbp)

        twi = QTableWidgetItem("Graph")
        twi.setFont(QFont("Times", 10, ))
        self.setItem(1,0,twi)


        dte = QDateTimeEdit()
        dte.setDateTime(QDateTime.currentDateTime())
        dte.setDisplayFormat("yyyy/MM/dd")
        dte.setCalendarPopup(True)
        self.setCellWidget(1,2,dte)

        cbw = QComboBox()
        cbw.addItem("a")
        cbw.addItem("b")
        cbw.addItem("c")
        self.setCellWidget(1,3,cbw)

        sb = QSpinBox()
        sb.setRange(1000,10000)
        sb.setValue(5000)
        sb.setDisplayIntegerBase(10)
        sb.setSuffix("c")
        sb.setPrefix("RMB: ")
        sb.setSingleStep(100)
        self.setCellWidget(1,4,sb)

        self.progressBar = QtWidgets.QProgressBar(self)
        self.progressBar.setProperty("value", 0)
        self.setCellWidget(0, 5, self.progressBar)

        self.progressBar = QtWidgets.QProgressBar(self)
        self.progressBar.setProperty("value", 0)
        self.setCellWidget(1, 5, self.progressBar)
        
        self.step = 0

        self.count=0
    def set_progress_bar_value(self,value):
        self.progressBar.setValue(value)
    '''