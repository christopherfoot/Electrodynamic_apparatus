#Start/stop button integrated, use with sketch30jan
import sys
import pyqtgraph as pg
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QVBoxLayout, QWidget, QPushButton, QGridLayout, QHBoxLayout, QVBoxLayout
from PyQt6.QtGui import QPalette, QColor
from PyQt6 import QtCore
import serial
import time




ser = serial.Serial('/dev/cu.usbmodem1301', 115200)
ser2 = serial.Serial('/dev/cu.usbmodem1401', 115200)



#==============================================
class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette) 

#==============================================

class MainWindow(QMainWindow):
    
        

    def __init__(self):
        super().__init__()
        self.resize(400, 200)

        self.setWindowTitle('Trap controls')
        layout = QVBoxLayout()
        layout1 = QHBoxLayout()
        layout2=QHBoxLayout()
        layout3=QHBoxLayout()
        layout4=QHBoxLayout()
        
        layout.addLayout(layout1)
        layout.addLayout(layout2)
        layout.addLayout(layout3)
        layout.addLayout(layout4)

        label = QLabel("Enter frequency")
        layout1.addWidget(label)

        self.input = QLineEdit()
        layout1.addWidget(self.input)
        

        self.btn = QPushButton("Start")
        layout2.addWidget(self.btn)
        self.btn.clicked.connect(self.send_func)

        self.btn2 = QPushButton("Stop")
        layout2.addWidget(self.btn2)
        self.btn2.clicked.connect(self.stop_func)

        #======================================
        self.reading_label = QLabel()
        self.reading_label.setWordWrap(False)
        layout4.addWidget(self.reading_label)

        self.lolol = Frequency_thread()
        self.lolol.freq_signal.connect(self.updatefreq)
        self.lolol.start()

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)


    def updatefreq(self,read_freq):
        if ser2.in_waiting >1:
           self.reading_label.setText("frequency is: "+str(read_freq)+"Hz")
        else:
            self.reading_label.setText("frequency is: null Hz")


    #==========================================
    

    def send_func(self):
        freq = self.input.text()
        
        freq_value = int(freq)
        if 10>freq_value>0:
            string = ('1000'+ str(freq))
        
        elif 100>freq_value>=10:
            string = ('100'+ str(freq))
        
        elif 300>freq_value>=100:
            freq_value=int(freq_value/0.9774)
            freq= str(freq_value)
            string = ('10'+ str(freq))

        elif 1000>freq_value>=300:
            freq_value=int(freq_value/0.948)
            freq= str(freq_value)
            string = ('10'+ str(freq))

        elif 10000>freq_value>=1000:
            freq_value=int(freq_value/0.669)
            freq= str(freq_value)
            string = ('1'+str(freq))

        ser.write(bytes(string,'UTF-8'))

    def stop_func(self):
        ser.write(bytes('0','UTF-8'))


class Frequency_thread(QtCore.QThread):
    freq_signal = QtCore.pyqtSignal(str)
    def __init__(self, parent=None):
        super(Frequency_thread,self).__init__(parent = parent)

    def run(self):
        while True:
            infreq = ser2.readline() 
            print(infreq)
            infreq = infreq.decode()
            
            self.freq_signal.emit(infreq)
            time.sleep(1)




app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
