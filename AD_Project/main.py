import pickle
import string
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QLayout, QGridLayout
from PyQt5.QtWidgets import QTextEdit, QLineEdit, QToolButton, QComboBox, QLabel, QScrollArea

from loadXlsx import LoadXlsx
from getName import PrintName


class Main(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.dbfilename = 'participation.dat'
        self.participation_list = []
        self.readParticipationList()

        self.fileNameBox = QLineEdit()
        self.fileNameBox.setMaxLength(256)
        self.fileNameBox.setFixedWidth(200)
        self.fileNameBox.setText("지하수로")
        self.fileNameBox.setAlignment(Qt.AlignRight)

        self.printArea = QScrollArea()
        self.printArea.setFixedHeight(450)
        self.printArea.setFixedWidth(300)


        self.nameArea = QLineEdit()
        self.nameArea.setFixedWidth(130)

        self.sortBox = QComboBox()
        self.sortBox.addItem("닉네임")
        self.sortBox.addItem("참여 횟수(오름차순)")
        self.sortBox.addItem("참여 횟수(내림차순)")
        self.sortBox.currentIndexChanged.connect(self.sorting)

        self.submitButton = QToolButton()
        self.submitButton.setText("파일 등록")
        self.submitButton.setFixedWidth(200)
        self.submitButton.clicked.connect(self.doSubmit)

        self.addButton = QToolButton()
        self.addButton.setText("횟수 추가")
        self.addButton.setFixedWidth(200)
        self.addButton.setFixedHeight(50)
        self.addButton.clicked.connect(self.doIncreaes)

        self.delButton = QToolButton()
        self.delButton.setText("횟수 감소")
        self.delButton.setFixedWidth(200)
        self.delButton.setFixedHeight(50)
        self.delButton.clicked.connect(self.doDecrease)

        self.printName = QToolButton()
        self.printName.setFixedWidth(200)
        self.printName.setFixedHeight(50)
        self.printName.setText("닉네임 출력")
        self.printName.clicked.connect(self.printOnlyName)

        self.currentStatus = QToolButton()
        self.currentStatus.setFixedWidth(200)
        self.currentStatus.setFixedHeight(50)
        self.currentStatus.setText("현재 참여 횟수")
        self.currentStatus.clicked.connect(self.printNameList)


        self.noParticipation = QToolButton()
        self.noParticipation.setFixedWidth(200)
        self.noParticipation.setFixedHeight(50)
        self.noParticipation.setText("0번 참여")
        self.noParticipation.clicked.connect(self.zeroParticipation)

        self.oneTimeParticipation = QToolButton()
        self.oneTimeParticipation.setFixedWidth(200)
        self.oneTimeParticipation.setFixedHeight(50)
        self.oneTimeParticipation.setText("한번 이하 참여")
        self.oneTimeParticipation.clicked.connect(self.underOneTimeParticipation)

        self.resetButton = QToolButton()
        self.resetButton.setText("Reset")
        self.resetButton.setFixedWidth(200)
        self.resetButton.clicked.connect(self.doReset)

        self.first_message = QLineEdit()
        self.first_message.setFixedWidth(200)

        printLayOut = QGridLayout()
        printLayOut.addWidget(QLabel("파일 이름:"), 0, 0)
        printLayOut.addWidget(self.fileNameBox, 0, 1)
        printLayOut.addWidget(QLabel(".xlsx"), 0 ,2)
        printLayOut.addWidget(self.printArea, 1, 0, 4, 0)

        buttonLayOut = QGridLayout()
        buttonLayOut.addWidget(QLabel("정렬기준: "), 0, 0)
        buttonLayOut.addWidget(self.sortBox, 0, 1)
        buttonLayOut.addWidget(QLabel("닉네임: "), 1, 0)
        buttonLayOut.addWidget(self.nameArea, 1, 1)
        buttonLayOut.addWidget(self.submitButton, 2,0,1,0)
        buttonLayOut.addWidget(self.addButton, 3,0,2,0)
        buttonLayOut.addWidget(self.delButton, 4,0,2,0)
        buttonLayOut.addWidget(self.printName, 5,0,2,0)
        buttonLayOut.addWidget(self.currentStatus, 6,0,2,0)
        buttonLayOut.addWidget(self.noParticipation,7,0,2,0)
        buttonLayOut.addWidget(self.oneTimeParticipation,8,0,2,0)
        buttonLayOut.addWidget(self.first_message,9,0,2,0)
        buttonLayOut.addWidget(self.resetButton,10,0,1,0)

        mainLayout = QGridLayout()
        mainLayout.setSizeConstraint(QLayout.SetFixedSize)
        mainLayout.addLayout(printLayOut,0,0)
        mainLayout.addLayout(buttonLayOut,0,1)

        self.setLayout(mainLayout)

        self.setWindowTitle("지하수로 출석부")

    def readParticipationList(self):
        try:
            fH = open(self.dbfilename, 'rb')
        except FileNotFoundError as e:
            self.participation_list = []
            return
        try:
            self.participation_list = pickle.load(fH)
        except:
            pass
        else:
            pass
        fH.close()

    def closeEvent(self,event):
        self.writeList()

    def writeList(self):
        fH = open("participation.dat", 'wb')
        pickle.dump(self.participation_list, fH)
        fH.close()

    def doSubmit(self):
        xlsx = LoadXlsx(self.fileNameBox.text())
        incList = xlsx.getName()
        for name in self.participation_list:
            if name["Name"] in incList:
                name["Participation"] += incList.count(name["Name"])
        self.printNameList()

    def doReset(self):
        reset = PrintName("nameList.txt")
        participation_list_reset = []
        nameList = reset.getNameList()
        print(nameList)
        for name in nameList:
            record = {"Name": name, "Participation" : 0}
            participation_list_reset += [record]
        self.participation_list = participation_list_reset
        self.printNameList()

    def doIncreaes(self):
        name = self.nameArea.text()
        for punc in string.punctuation:
            if punc in name:
                self.first_message.setText("Wrong Nickname!")
                return
        for p in self.participation_list:
            if p["Name"] == name:
                p["Participation"] += 1
        self.printNameList()

    def doDecrease(self):
        name = self.nameArea.text()
        for punc in string.punctuation:
            if punc in name:
                self.first_message.setText("Wrong Nickname!")
                return
        for p in self.participation_list:
            if p["Name"] == name:
                if p["Participation"] == 0:
                    self.first_message.setText("Can't Decrease Under 0")
                else:
                    p["Participation"] -= 1
        self.printNameList()

    def printOnlyName(self):
        rString = ""
        for name in self.participation_list:
            rString += ("Name : " + str(name["Name"]) + '\n')
        self.showList(rString)

    def printNameList(self):
        print(self.participation_list)
        rString = ""

        for name in self.participation_list:
            if len(name["Name"]) > 9:
                rString += ("Name : " + str(name["Name"]) + '\t' + str(name["Participation"]))
            else:
                rString += ("Name : " + str(name["Name"]) + '\t\t' + str(name["Participation"]))
            rString += '\n'
        self.showList(rString)

    def showList(self, string):
        self.printArea.setWidget(QLabel(string))

    def zeroParticipation(self):
        rString = ""
        for name in self.participation_list:
            if name["Participation"] == 0:
                if len(name["Name"]) > 9:
                    rString += ("Name : " + str(name["Name"]) + '\t' + str(name["Participation"]))
                else:
                    rString += ("Name : " + str(name["Name"]) + '\t\t' + str(name["Participation"]))
                rString += '\n'
        self.showList(rString)

    def underOneTimeParticipation(self):
        rString = ""
        for name in self.participation_list:
            if name["Participation"] <= 1:
                if len(name["Name"]) > 9:
                    rString += ("Name : " + str(name["Name"]) + '\t' + str(name["Participation"]))
                else:
                    rString += ("Name : " + str(name["Name"]) + '\t\t' + str(name["Participation"]))
                rString += '\n'
        self.showList(rString)
        
    def sorting(self):
        if self.sortBox.currentIndex() == 0:
            self.participation_list.sort(key = lambda name : name["Name"])
        elif self.sortBox.currentIndex() == 1:
            self.participation_list.sort(key = lambda name : name["Participation"])
        else:
            self.participation_list.sort(key = lambda name : name["Participation"], reverse = True)


if __name__ == '__main__':

    import sys
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())
