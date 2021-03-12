import sys 
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtCore import QDate, QTime, QDateTime, Qt,QFile,QThread
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QMessageBox
from PyQt5.QtWidgets import* 
from PyQt5.uic import loadUi
import struct
import os
import sys
import glob
import xml.etree.ElementTree as ET
import string
import resource
import time
import serial
from serial import SerialException
import serial.tools.list_ports
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
from numpy import array
from PyQt5.QtCore import pyqtSignal




import numpy as np
class dataprocess(QThread):
    progress = pyqtSignal(int)
    convert_finish = pyqtSignal(str,bool)
    def __init__(self):
        QThread.__init__(self)
        self.content = ""
        self.filename = ""
        #self.result_file
        self.running = True
        self.filenames = list()
    def __del__(self):
        self.wait()
    def setport(self,serial_port):
        self.ser = serial_port
        
    def stop(self):
        pass
    
    def reset_cmd(self):
        pass
        #send reset command for restart a new record
    def inputfiles(self,filenames):
        self.filenames = filenames
        pass
    
    def save_file(self,name,data):
        try:
            if not os.path.exists("./Result"):
                os.makedirs("./Result")
        except OSError:
            print ('Error: Creating directory. ' + "./Result")
            
        time=QDateTime.currentDateTime()
        timeDisplay=time.toString('yyyyMMddhhmmss')

        name = name.split('/')[-1]
        name = name.replace(".log","")        
        try:
             try:
                 if not os.makedirs("./Result/"+name):
                     os.makedirs("./Result")
             except:
                 print("exist")
             self.result_file= open("./Result/"+name+"/result_"+timeDisplay + ".log",'w')
             self.result_file.write(data)
             self.result_file.close()
        except:
            print("pk")
        
    def parser_logfile(self,name):
        try:
            f = open(name,'r')
            file = f.read()
            return file
        except:
            print("read file failed.")

    def process(self):
        if self.filenames is not None:
            for i in self.filenames:
                
                file = self.parser_logfile(i)
                
                data = self.fetch_data_process(file)
                self.save_file(i,data)

        else:
            print("filename error")
        direct = "./Result"
        self.convert_finish.emit(direct,True)
    def fetch_data_process(self,content):
        row = content.split('\n')
        total_count = len(content)
        count = 0
        mcount =  int(total_count/100)
        writestr = ""
        for i in row:
            seg = i.split(",")
            #print("-----")
            pressure = int(seg[1])
            pressure = np.int32(pressure)
            #print(pressure)
            accx = int(seg[2])
            accx = np.int16(accx)
            
            accy = int(seg[3])
            accy = np.int16(accy)
            accz = int(seg[4])
            accz = np.int16(accz)
            
            a = struct.pack("i",pressure)
            b = struct.pack("h",accx)
            c = struct.pack("h",accy)
            d = struct.pack("h",accz)
            checksum = 0x55 + 0x0f + 0x03 + sum(a) + sum(b) + sum(c) + sum(d)
            checksum = np.uint32(checksum)
            
            b = struct.pack('<bbbihhhI',0x55,0x0f,0x03,pressure,accx,accy,accz,checksum)
            count = count +1
            #print(count,":   " , b.hex())
            #self.ser.flush()
            self.ser.write(b)
            ack = self.ser.read(11)
            header,len_,type_,bpm,rpm,bpm_pre,status,checksum = struct.unpack("<bbbbbbbI",ack)
            #print(len(ack),ack)
            #print("bpm =",bpm,"rpm = ",rpm,"bpm_pre=", bpm_pre,"status",status)
            
            writestr = writestr+ "%s,%s,%s,%s\n"%(str(bpm),str(rpm),str(bpm_pre),str(status))
            #self.result_file.write(writestr)  
            if count % (mcount) == 0:
                pro = count*100 / total_count
                print(pro)
                self.progress.emit(int(pro))  
            time.sleep(0.01)  # 1/256
        self.progress.emit(int(100))

        return writestr
    def run(self):
        #run a batch of files
        self.process()

class MyForm(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        loadUi("playback.ui",self)
        #self.populate()
        
        self.find_ports()
        self.slot_initialize()
        self.plot_initialize()
        
        self.ser=serial.Serial()
        self.file_list=list()
    def slot_initialize(self):
        self.removefile_pushButton.clicked.connect(self.remove_file)
        self.addfile_pushButton.clicked.connect(self.add_record_file)
        self.connect_pushButton.clicked.connect(self.port_connect)
        self.disconnect_pushButton.clicked.connect(self.port_disconnect)
        self.start_pushButton.clicked.connect(self.start_process)
        self.dataprocess_thread = dataprocess()
        self.dataprocess_thread.progress.connect(self.update_progressbar)
        self.dataprocess_thread.convert_finish.connect(self.update_directory_treeview)
        self.stop_pushButton.clicked.connect(self.stop_process)
        self.setWindowIcon(QtGui.QIcon(":/icon/logo.png"))
        self.disconnect_pushButton.setEnabled(False)
        self.progressBar.setValue(0)
        self.outputdir_Button.clicked.connect(self.update_output_directory)
        self.outputdir_lineEdit.setText("./")
        self.update_directory_treeview("./",True)
        
        self.output_result_checkBox.setChecked(True)
        self.recursive_test_checkBox.setChecked(True)
        self.reset_test_checkBox.setChecked(True)
        
        self.treeView.doubleClicked.connect(self.test)
    def test(self,index):
        print(self.treeView.model().data(index))

        #self.treeView.expandAll()
        #data = index.model().data(index)
        #data = self.treeView.model().data(index)
        #self.treeView.
        #print(type(index))
    def plot_initialize(self):
        pass
        '''
        self.p1 = pg.PlotWidget()
        self.p2 = pg.PlotWidget()
        self.p3 = pg.PlotWidget()

        self.p1.setTitle("pressure")
        self.p2.setTitle("accelerameter")
        
        self.p1.setLabel('left', "(ADC)")
        self.p1.setLabel('bottom', "(s)")
        
        self.p2.setLabel('left', "(ADC)")
        self.p2.setLabel('bottom', "(s)")
        
        self.p1.addLegend()
        self.p2.addLegend()
        
        self.plot_Layout.addWidget(self.p1)
        self.plot_Layout.addWidget(self.p2)
        self.plot_Layout.addWidget(self.p3)
        self.plot_preesure_data([1,2,3])
        '''
    def plot_preesure_data(self,data):
        self.p1.plot(data)

    def pasrser_file(self,filename):
        
        pass
        
        
    def update_progressbar(self,count):
        print(count)
        self.progressBar.setValue(count)
        
        
    def update_output_directory(self):
        folderpath = QFileDialog.getExistingDirectory(self, 'Select Output Folder')
        self.update_directory_treeview(folderpath,True)
        self.outputdir_lineEdit.setText(folderpath)
        
        
    def update_directory_treeview(self,direct,flag):
        if flag == True:
            path = direct
            self.model = QFileSystemModel()
            self.model.setRootPath((QtCore.QDir.rootPath()))
            self.treeView.setModel(self.model)
            self.treeView.setRootIndex(self.model.index(path))
            self.treeView.setSortingEnabled(True)
    
    
    def start_process(self) :
        self.dataprocess_thread.setport(self.ser)
        count = self.listWidget.count()
        self.file_list=list()
        for i in range(count):
            self.listWidget.item(i)
            self.file_list.append(self.listWidget.item(i).text())
        self.dataprocess_thread.inputfiles(self.file_list)
        self.dataprocess_thread.start()
        '''
        if self.listWidget.count !=0:
            filename = self.listWidget.item(0)
            if filename != None:
                self.dataprocess_thread.inputfile(filename.text())
                fstr = filename.text()
                print(fstr)
                fstr = fstr.split("/")[-1]
                self.filename_label.setText(fstr)
                self.dataprocess_thread.start()
        '''
    def stop_process(self):
        print("finish data")
        self.dataprocess_thread.terminate()
        
        
    def add_record_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog  
        caption = 'Open file'
        directory = ''
        filter_mask = "Python/Text files (*.log *.xml *.txt)"
        filenames = QFileDialog.getOpenFileNames(None,caption, directory, filter_mask)[0]
        #add multiple files       
        #self.listWidget.addItems(filenames)
        
        # do not add duplicate files
        for i in filenames:
            if not self.listWidget.findItems(i, Qt.MatchFixedString | Qt.MatchCaseSensitive):
                self.listWidget.addItem(i)
            #filename = QtCore.QFileInfo(i).fileName()
            #self.listWidget.addItem(i)

    def port_connect(self):
        comport = self.comport_comboBox.currentText()
        baudrate  = self.baudrate_comboBox.currentText()
        baudrate = int(baudrate)
        self.comport_name = str(comport)
        try:
            if self.ser.is_open is False:
                self.ser=serial.Serial(self.comport_name,baudrate) 
                self.disconnect_pushButton.setEnabled(True)
                print(self.ser.is_open)
        except:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Critical)
            msgBox.setText("Serial port not found!")
            msgBox.setWindowTitle("Error")
            msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            returnValue = msgBox.exec()
            self.disconnect_pushButton.setEnabled(False)
            self.find_ports()
               
               
    def port_disconnect(self):
        if self.ser.is_open:
            self.ser.close()
            self.disconnect_pushButton.setEnabled(False)
            print(self.ser.is_open)
        
    def find_ports(self):
        
    
        self.comport_comboBox.clear() 
        QApplication.setOverrideCursor(Qt.WaitCursor)
        ports = serial.tools.list_ports.comports(include_links=False)
        
        for port in ports :
           self.comport_comboBox.addItem(port.device)
        QApplication.restoreOverrideCursor()
        
    def remove_file(self):
        self.listWidget.takeItem(self.listWidget.currentRow())
        
    
if __name__=="__main__":

    app = QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon("/icon/logo.png"))
    ex=MyForm()
    ex.show()
    sys.exit(app.exec_())
            
