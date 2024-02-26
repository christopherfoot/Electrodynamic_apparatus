"""
Version1.0.4 specifics:
- voltage control
- frequency control
- graph monitor for reader frequency
compatible arduino codes:
- for control: control1.0.2.ino 
- for reader: Monitor1.0.1.ino
"""
"""
Author: Francesco Straniero
Date: 26/02/2024

HOW DOES THIS APP WORK:
for a detailed description refer to https://github.com/christopherfoot/Electrodynamic_apparatus 
This python application onsists of the User interface to control the electronics for an electrodynamic trap, 
the code is structured using different threads of execution, so that the application can 'simultaneously' send signals to the arduino, and read back from the other arduino.
Required libraries to install before are:
- PyQt6
- pyqtgraph
- serial 
useful resources to learn about these libraries:
- https://www.pythonguis.com/tutorials/pyqt6-creating-your-first-window/
- https://realpython.com/python-pyqt-qthread/#communicating-with-worker-qthreads
- https://dlcoder.medium.com/using-pyserial-in-python-a-comprehensive-guide-2874c5388454#:~:text=ser.close()-,Reading%20and%20Writing%20Data,newline%20character%20(%20%5Cn%20).

VERY IMPORTANT THINGS TO NOTE:
- for this version, the serial ports used must be declared in this script: in lines 36/37 declare which port you are using with the arduino.
- sometimes the graph might stop uploading, this is because there might be some wrong bytes coming from the arduino or some old bytres in the serial buffer. However, since the graph runs on a separate thread of execution, this problem will not stop the main part of the application from running.
"""

import sys
import pyqtgraph as pg
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QVBoxLayout, QWidget, QPushButton, QGridLayout, QHBoxLayout, QVBoxLayout
from PyQt6.QtGui import QPalette, QColor
from PyQt6 import QtCore
import serial
from random import randint
import time

#these next two lines open serial communication with the arduino boards
ser = serial.Serial('/dev/cu.usbmodem11301', 115200) #control arduino
ser2 = serial.Serial('/dev/cu.usbmodem11401', 115200) #monitor arduino



#==============================================
class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette) 

#==============================================
#THIS NEXT PART DEFINES THE GUI
class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.resize(600, 400)

        self.setWindowTitle('Trap controls')
        layout = QVBoxLayout()
        layout0 =QHBoxLayout()
        layout1 = QHBoxLayout()
        layout2=QHBoxLayout()
        layout3=QHBoxLayout()
        layout4=QHBoxLayout()
        layout5 = QHBoxLayout()
        layout6=QHBoxLayout()
        layout7=QHBoxLayout()
        layout8=QHBoxLayout()
        
        layout.addLayout(layout0) #control description
        layout.addLayout(layout1) #Input frequency
        layout.addLayout(layout6) #power entry
        layout.addLayout(layout2) #start/stop buttons
        layout.addLayout(layout3) 
        layout.addLayout(layout5) #monitor label
        layout.addLayout(layout4) #monitor graph
        layout.addLayout(layout7)
        layout.addLayout(layout8)

        label1 =QLabel("Trap controls (when pressing start, make sure both entries are filled)")
        label1.setStyleSheet("background-color: blue")
        layout0.addWidget(label1)
        

        label = QLabel("Enter frequency")
        layout1.addWidget(label)

        self.input_frequency = QLineEdit()
        layout1.addWidget(self.input_frequency)

        label3 =QLabel("Enter Voltage percentage (0-100)")
        layout6.addWidget(label3)

        self.input_voltage = QLineEdit()
        self.input_voltage.setPlaceholderText('please enter 99 as 099')
        layout6.addWidget(self.input_voltage)

        self.btn = QPushButton("Start")
        layout2.addWidget(self.btn)
        self.btn.clicked.connect(self.send_func)

        self.btn2 = QPushButton("Stop")
        layout2.addWidget(self.btn2)
        self.btn2.clicked.connect(self.stop_func)

        #======================================
        #GRAPH SECTION

        label2 =QLabel("Monitor")
        label2.setStyleSheet("background-color: blue")
        layout5.addWidget(label2)

        self.plot_graph = pg.PlotWidget()
        layout4.addWidget(self.plot_graph)
        self.time = list(range(200))
        
        self.temperature = [1000 for _ in range(200)]
        self.line = self.plot_graph.plot(self.time, self.temperature)
        self.timer = QtCore.QTimer()
        self.timer.setInterval(300)
        #self.timer.timeout.connect(self.update_plot)
        self.timer.start()

        self.lolol = Frequency_thread()
        self.lolol.freq_signal.connect(self.update_plot)
        self.lolol.start()

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    #=======================================================================
    #THE NEXT PART CONSISTS OF THE VARIOUS FUNCTIONS WHICH ARE ACTIVATED WHEN BUTTONS ARE PRESSED.

    def update_plot(self, message):                      #updates the graph
        
        self.time = self.time[1:]
        self.time.append(self.time[-1] + 1)
        self.temperature = self.temperature[1:]
        self.temperature.append(message)
        self.line.setData(self.time, self.temperature)
    

    def send_func(self):                                  #sends input frequency to arduino
        freq = self.input_frequency.text()
        voltage = self.input_voltage.text()
        
        freq_value = int(freq)
        if 10>freq_value>0:
            string = ('1000'+ str(freq)+'0'+str(voltage))
        
        elif 100>freq_value>=10:
            string = ('100'+ str(freq)+'0'+str(voltage))
        
        elif 300>freq_value>=100:
            freq_value=int(freq_value) #/0.9774)
            freq= str(freq_value)
            string = ('10'+ str(freq)+'0'+str(voltage))

        elif 1000>freq_value>=300:
            freq_value=int(freq_value) #/0.948)
            freq= str(freq_value)
            string = ('10'+ str(freq)+'0'+str(voltage))

        elif 10000>freq_value>=1000:
            freq_value=int(freq_value) #/0.669)
            freq= str(freq_value)
            string = ('1'+str(freq)+'0'+str(voltage))

        ser.write(bytes(string,'UTF-8'))
        

    def stop_func(self):                              #sends stop signal to arduino
        ser.write(bytes('0000000000','UTF-8'))

#=======================================================================================
#SEPARATE THREAD OF EXECUTION: 
#this next part is a different thread of execution (aka a part of the program which runs parallel to the main program)
#this parts reads the signals from the second arduino and then sends them to the graph function
class Frequency_thread(QtCore.QThread):
    freq_signal = QtCore.pyqtSignal(int)
    def __init__(self, parent=None):
        super(Frequency_thread,self).__init__(parent = parent)

    def run(self):
        while True:
            if ser2.in_waiting >6:
                
                infreq = ser2.readline()
            
                infreq = infreq.decode()
                infreq = int(infreq.strip())  
                self.freq_signal.emit(infreq)
            else:                                 #not sure if this 'else' is actually needed
                self.freq_signal.emit(0)
            
            




app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()