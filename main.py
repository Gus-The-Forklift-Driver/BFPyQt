import sys

from PyQt5 import QtWidgets, uic, QtCore

from BFI import programRunner

bfi = programRunner(consoleOutput=True, memoryRollover=False)


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('v1.ui', self)
        self.show()
        self.findChild(QtWidgets.QPushButton, 'run').clicked.connect(self.runButtonClicked)
        self.findChild(QtWidgets.QPushButton, 'step').clicked.connect(self.stepButtonClicked)
        self.findChild(QtWidgets.QPushButton, 'stop').clicked.connect(self.stopButtonClicked)
        self.findChild(QtWidgets.QSpinBox, 'delay').valueChanged.connect(self.updateDelay)

        self.runButton = self.findChild(QtWidgets.QPushButton, 'run')
        self.stepButton = self.findChild(QtWidgets.QPushButton, 'step')
        self.stopButton = self.findChild(QtWidgets.QPushButton, 'stop')

        self.runButton.clicked.connect(self.runButtonClicked)
        self.stepButton.clicked.connect(self.stepButtonClicked)

        self.running = False
        self.programActive = False

        self.timer = QtCore.QTimer()
        self.timer.setInterval(10)
        self.timer.timeout.connect(self.uiUpdate)
        self.timer.start()

    def runButtonClicked(self):
        self.runButton.clicked.disconnect()
        self.runButton.setText("Pause")
        self.runButton.clicked.connect(self.pauseButtonClicked)

        self.running = True
        self.stopButton.setEnabled(True)

        if not self.programActive:
            bfi.cleanup()
            bfi.setProgram(self.findChild(QtWidgets.QPlainTextEdit, 'program').toPlainText())
            self.findChild(QtWidgets.QPlainTextEdit, 'memory').setPlainText(str(bfi.memory))

    def pauseButtonClicked(self):
        self.runButton.clicked.disconnect()
        self.runButton.setText("Continue")
        self.runButton.clicked.connect(self.runButtonClicked)

        self.running = True
        self.programActive = True

    def stepButtonClicked(self):

        if not self.programActive:
            bfi.cleanup()
            bfi.setProgram(self.findChild(QtWidgets.QPlainTextEdit, 'program').toPlainText())
            self.findChild(QtWidgets.QPlainTextEdit, 'memory').setPlainText(str(bfi.memory))
            self.stopButton.setEnabled(True)
            self.programActive(True)

        self.running = False

        if bfi.programPointer < len(bfi.program):
            bfi.step()
            if bfi.consoleOutput:
                print(bfi.consoleContent)
        else:
            self.runButton.clicked.disconnect()
            self.runButton.setText("Run")
            self.runButton.clicked.connect(self.runButtonClicked)

            self.stopButton.setEnabled(False)
            self.running = False
            self.programActive = False

    def stopButtonClicked(self):
        self.runButton.clicked.disconnect()
        self.runButton.setText("Run")
        self.runButton.clicked.connect(self.runButtonClicked)

        self.running = False
        self.programActive = False
        bfi.needInput = False
        self.stopButton.setEnabled(False)
        self.stepButton.setEnabled(True)
        self.runButton.setEnabled(True)
        self.findChild(QtWidgets.QLineEdit, 'input').setEnabled(False)
        # self.findChild(QtWidgets.QPlainTextEdit, 'memory').setPlainText(str(bfi.memory))

    def uiUpdate(self):
        if bfi.needInput:
            bfi.memory[bfi.memoryPointer] = self.handleInput()
        if self.running:
            if not bfi.programPointer < len(bfi.program):
                self.runButton.clicked.disconnect()
                self.runButton.setText("Run")
                self.runButton.clicked.connect(self.runButtonClicked)

                self.stopButton.setEnabled(False)
                self.running = False
                self.programActive = False

            else:
                bfi.step()

                self.findChild(QtWidgets.QPlainTextEdit, 'memory').setPlainText(str(bfi.memory))
                self.findChild(QtWidgets.QLabel, 'output').setText(bfi.output)
                if bfi.consoleOutput:
                    print(bfi.consoleContent)

    def updateDelay(self):
        self.timer.setInterval(self.findChild(QtWidgets.QSpinBox, 'delay').value())

    def handleInput(self):

        self.runButton.clicked.disconnect()
        self.runButton.setText("Continue")
        self.runButton.clicked.connect(self.runButtonClicked)

        self.stepButton.setEnabled(False)
        self.runButton.setEnabled(False)
        self.findChild(QtWidgets.QLineEdit, 'input').setEnabled(True)
        while True:
            try:
                value = ord(self.findChild(QtWidgets.QLineEdit, 'input').text())
            except:
                pass
            else:
                self.findChild(QtWidgets.QLineEdit, 'input').setText("")
                self.findChild(QtWidgets.QLineEdit, 'input').setEnabled(False)
                self.stepButton.setEnabled(True)
                self.runButton.setEnabled(True)
                bfi.needInput = False
                break
            app.processEvents()
        return value


app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
#input("press enter to exit")
