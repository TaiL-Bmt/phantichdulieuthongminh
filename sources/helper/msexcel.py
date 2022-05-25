import openpyxl

class MsExcelLoaderForDA:
    def __init__(self):
        self.__result = None
        
    def GetData(self):
        return self.__result
        
    def LoadFile(self, path, workSheetName, firstRowHeader):
        self.__result = None
    
        wb = openpyxl.load_workbook(path)
        sheet = wb[workSheetName]

        maxNCol = 0
        rows = []
        xRows = sheet.iter_rows()
        for xRow in xRows:
            cells = []
            for xCell in xRow:
                cells.append(xCell.value)
            rows.append(cells)
            
            nCol = len(cells)
            if nCol > maxNCol:
                maxNCol = nCol

        for row in rows:
            cells = row
            i = len(cells)
            while i < maxNCol:
                cells.append('')
                i = i + 1

        colNames = None
        result = None
        for row in rows:
            if result is None:
                if firstRowHeader:
                    result = {}
                    colNames = row
                    for name in colNames:
                        values = []
                        result[name] = values
                    continue
                else:
                    result = []
                    i = 0
                    while i < maxNCol:
                        values = []
                        result.append(values)
                        i = i + 1

            i = 0
            while i < maxNCol:
                values = None
                if colNames is None:
                    values = result[i]
                else:
                    values = result[colNames[i]]
                values.append(row[i])
                i = i + 1

        self.__result = result
        return result

    def ToFloatArrayVN(self, ar):
        n = len(ar)
        i = 0
        while i < n:
            s = str(ar[i])
            s = s.replace(',', '#')
            s = s.replace('.', '')
            s = s.replace('#', '.')
            ar[i] = float(s)
            i = i + 1
        return ar