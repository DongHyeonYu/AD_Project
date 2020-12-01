from openpyxl import load_workbook

class LoadXlsx:
    def __init__(self,filename):
        self.load_name = load_workbook(filename +".xlsx", data_only = True)
        self.name_list = []
    def getName(self):
        weekList = ['1주차', '2주차', '3주차', '4주차', '5주차']
        cell_list = []
        for column in ['A', 'G', 'M']:
            for row in range(10, 63, 2):
                if (row - 22) % 14 == 0 : continue
                else:
                    cell_list += [column + str(row)]

        for week in weekList:
            load_name_sheet = self.load_name[week]
            for cell in cell_list:
                if load_name_sheet[cell].value != None:
                    self.name_list += [load_name_sheet[cell].value]
        return self.name_list

