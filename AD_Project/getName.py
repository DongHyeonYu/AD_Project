class PrintName:
    def __init__(self,filename):
        self.nameList = []
        f = open(filename, 'r')
        lines = f.readlines()
        f.close()

        self.count = 0
        for line in lines:
            word = line.rstrip()
            self.nameList.append(word)

    def getNameList(self):
        rList = []
        for name in self.nameList:
            rList.append(name)
        return rList