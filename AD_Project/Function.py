import pickle
import string

from loadXlsx import LoadXlsx
from getName import PrintName

class Function:
    def __init__(self,filename):
        self.filename = filename
        self.xlsx = LoadXlsx(self.filename)
        self.reset = PrintName("nameList.txt")
        self.participation_list = []
        self.readParticipationList()

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
        try:
            incList = self.xlsx.getName()
            for name in self.participation_list:
                if name["Name"] in incList:
                    name["Participation"] += incList.count(name["Name"])
            self.printNameList()
        except FileNotFoundError:
            return "FileNotFoundError!"

    def doReset(self):
        participation_list_reset = []
        nameList = self.reset.getNameList()
        for name in nameList:
            record = {"Name": name, "Participation" : 0}
            participation_list_reset += [record]
        self.participation_list = participation_list_reset
        self.printNameList()

    def doIncreaes(self):
        name = self.nameArea.text()
        for punc in string.punctuation:
            if punc in name:
                return "Wrong Nickname!"
        for p in self.participation_list:
            if p["Name"] == name:
                if p["Participation"] == 5:
                    self.first_message.setText("Can't Increase More than 5")
                else:
                    p["Participation"] += 1
        self.printNameList()

    def doDecrease(self):
        name = self.nameArea.text()
        for punc in string.punctuation:
            if punc in name:
                return "Wrong Nickname!"
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
        return rString

    def zeroParticipation(self):
        rString = ""
        for name in self.participation_list:
            if name["Participation"] == 0:
                if len(name["Name"]) > 9:
                    rString += ("Name : " + str(name["Name"]) + '\t' + str(name["Participation"]))
                else:
                    rString += ("Name : " + str(name["Name"]) + '\t\t' + str(name["Participation"]))
                rString += '\n'
        return rString

    def underOneTimeParticipation(self):
        rString = ""
        for name in self.participation_list:
            if name["Participation"] <= 1:
                if len(name["Name"]) > 9:
                    rString += ("Name : " + str(name["Name"]) + '\t' + str(name["Participation"]))
                else:
                    rString += ("Name : " + str(name["Name"]) + '\t\t' + str(name["Participation"]))
                rString += '\n'
        return rString

    def printNameList(self):
        rString = ""
        for name in self.participation_list:
            if len(name["Name"]) > 9:
                rString += ("Name : " + str(name["Name"]) + '\t' + str(name["Participation"]))
            else:
                rString += ("Name : " + str(name["Name"]) + '\t\t' + str(name["Participation"]))
            rString += '\n'
        self.sorting()
        return rString

    def sorting(self):
        if self.sortBox.currentIndex() == 0:
            self.participation_list.sort(key = lambda name : name["Name"])
        elif self.sortBox.currentIndex() == 1:
            self.participation_list.sort(key = lambda name : name["Participation"])
        else:
            self.participation_list.sort(key = lambda name : name["Participation"], reverse = True)


