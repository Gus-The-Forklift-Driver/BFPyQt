from PyQt5.QtCore import pyqtSignal,QObject


class programRunner:
    memoryPointer = 0
    programPointer = 0
    bracemap = []
    consoleContent = ""

    def __init__(self, program="", memory=[], memorySize=250, consoleOutput=False, memoryRollover=False):

        self.program = ''.join(filter(lambda x: x in ['.', ',', '[', ']', '<', '>', '+', '-'], program))
        self.memory = memory
        self.memorySize = memorySize
        self.memoryRollover = memoryRollover
        self.consoleOutput = consoleOutput
        self.output = ""
        self.needInput = False

        #fill the memory
        if len(self.memory) == 0:
            for x in range(self.memorySize):
                self.memory.append(0)
        else:
            if len(self.memory) <= self.memorySize:
                for x in range(self.memorySize - len(self.memory)):
                    self.memory.append(0)


    def step(self):
        instruction = self.program[self.programPointer]
        self.memory[self.memoryPointer] = self.memory[self.memoryPointer]

        if instruction == '+':
            self.memory[self.memoryPointer] += 1
            if self.memory[self.memoryPointer] > 256 and self.memoryRollover:
                self.memory[self.memoryPointer] = 0
            self.consoleContent = "add at adress : " + str(self.memoryPointer)

        elif instruction == '-':

            if self.memory[self.memoryPointer] <= 0 and self.memoryRollover:
                self.memory[self.memoryPointer] = 256
            self.memory[self.memoryPointer] -= 1
            self.consoleContent = "sub at adress : " + str(self.memoryPointer)

        elif instruction == '>':
            self.memoryPointer += 1
            self.consoleContent = "Move to : " + str(self.memoryPointer)

        elif instruction == '<':
            self.memoryPointer -= 1
            self.consoleContent = "Move to : " + str(self.memoryPointer)

        elif instruction == '[':
            self.bracemap.append(self.programPointer)
            self.consoleContent = "Added adress : " + str(self.bracemap[-1])

        elif instruction == ']':
            if self.memory[self.memoryPointer] == 0:
                self.consoleContent = "removed adress : " + str(self.bracemap.pop())

            else:
                self.programPointer = self.bracemap[-1]
                self.consoleContent = "Jump to : " + str(self.bracemap[-1])

        elif instruction == '.':
            self.output += chr((self.memory[self.memoryPointer]))
            self.consoleContent = "Output" + chr(self.memory[self.memoryPointer])

        elif instruction == ',':
            self.needInput = True
            self.consoleContent = "Input"

        self.programPointer += 1

    def runCode(self):
        while self.programPointer < len(self.program):
            self.step()
            if self.consoleOutput:
                print(self.consoleContent)

    def cleanup(self):
        self.programPointer = 0
        self.memoryPointer = 0
        self.needInput = False
        self.memory = []



        for x in range(self.memorySize):
            self.memory.append(0)

    def setProgram(self,prog):
        self.program = ''.join(filter(lambda x: x in ['.', ',', '[', ']', '<', '>', '+', '-'], prog))