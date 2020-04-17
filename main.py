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

        self.running = False
        self.programActive = False

        self.timer = QtCore.QTimer()
        self.timer.setInterval(10)
        self.timer.timeout.connect(self.uiUpdate)
        self.timer.start()

    def runButtonClicked(self):
        if self.running:
            self.findChild(QtWidgets.QPushButton, 'run').setText("Run")
            self.running = False
            if not self.programActive:
                self.findChild(QtWidgets.QPushButton, 'stop').setEnabled(False)

        else:
            self.findChild(QtWidgets.QPushButton, 'run').setText("Pause")
            self.findChild(QtWidgets.QPushButton, 'stop').setEnabled(True)
            self.running = True
            self.programActive = True
            if self.programActive:
                bfi.cleanup()
                bfi.setProgram(self.findChild(QtWidgets.QPlainTextEdit, 'program').toPlainText())
                self.findChild(QtWidgets.QPlainTextEdit, 'memory').setPlainText(str(bfi.memory))

    def stepButtonClicked(self):
        if bfi.programPointer < len(bfi.program) and not self.running and self.programActive:
            if self.running:
                self.findChild(QtWidgets.QPushButton, 'run').setText("Continue")
                self.running = False
            bfi.step()
            self.findChild(QtWidgets.QPlainTextEdit, 'memory').setPlainText(str(bfi.memory))
            if bfi.consoleOutput:
                print(bfi.consoleContent)

        elif not self.programActive:
            bfi.cleanup()
            bfi.setProgram(self.findChild(QtWidgets.QPlainTextEdit, 'program').toPlainText())
            self.findChild(QtWidgets.QPlainTextEdit, 'memory').setPlainText(str(bfi.memory))
            self.findChild(QtWidgets.QPushButton, 'stop').setEnabled(True)
            self.programActive = True

    def stopButtonClicked(self):
        self.findChild(QtWidgets.QPushButton, 'run').setText("Run")
        self.findChild(QtWidgets.QPushButton, 'stop').setEnabled(False)
        self.running = False
        self.programActive = False

        self.findChild(QtWidgets.QPlainTextEdit, 'memory').setPlainText(str(bfi.memory))

    def uiUpdate(self):
        if bfi.needInput:
            bfi.memory[bfi.memoryPointer] = self.handleInput()
        if self.running:
            if not bfi.programPointer < len(bfi.program):
                self.running = False
                self.programActive = False
                self.findChild(QtWidgets.QPushButton, 'run').setText("Run")
                self.findChild(QtWidgets.QPushButton, 'stop').setEnabled(False)
            else:
                bfi.step()

                self.findChild(QtWidgets.QPlainTextEdit, 'memory').setPlainText(str(bfi.memory))
                self.findChild(QtWidgets.QLabel, 'output').setText(bfi.output)
                if bfi.consoleOutput:
                    print(bfi.consoleContent)

    def updateDelay(self):
        self.timer.setInterval(self.findChild(QtWidgets.QSpinBox, 'delay').value())

    def handleInput(self):
        # self.timer.stop()
        self.running = False
        self.findChild(QtWidgets.QPushButton, 'run').setText("Continue")
        while True:
            try:
                value = ord(self.findChild(QtWidgets.QLineEdit, 'input').text())
            except:
                pass
            else:
                break
            app.processEvents()
        # self.timer.start()
        # self.findChild(QtWidgets.QLineEdit, 'input').setText("")
        self.running = True
        return value


app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
