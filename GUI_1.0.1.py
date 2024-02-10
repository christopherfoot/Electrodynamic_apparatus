#Start/stop button integrated, use with sketch30jan
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QVBoxLayout, QWidget, QPushButton, QGridLayout, QHBoxLayout, QVBoxLayout
from PyQt6.QtGui import QPalette, QColor
import serial

ser = serial.Serial('/dev/cu.usbmodem1301', 115200) #Starts serial communication to send out signals

#=========================================================

class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette) 

#=========================================================
""" This part of the code is the GUI, """

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(400, 200)

        self.setWindowTitle('Trap controls')
        layout = QVBoxLayout()
        layout1 = QHBoxLayout()
        layout2=QHBoxLayout()
        layout3=QHBoxLayout()


        layout.addLayout(layout1)
        layout.addLayout(layout2)
        layout.addLayout(layout3)

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

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
    #========================================================
    """This next part of the code sends a string of values corresponding to the frequency, it starts with a 1 
    so that the arduino starts  """
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

        #print(string)
        ser.write(bytes(string,'UTF-8'))

    def stop_func(self):
        ser.write(bytes('0','UTF-8'))          #The 0 tells the arduino to stop



#=========================================================       

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
