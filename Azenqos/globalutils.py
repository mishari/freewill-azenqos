from PyQt5.QtSql import QSql, QSqlDatabase, QSqlQuery
import csv, inspect, os
from zipfile import ZipFile
from dataclasses import dataclass

db = None
elementData = []


def lineno():
    """Returns the current line number in our program."""
    return inspect.currentframe().f_back.f_lineno


# todo: ใช้ข้อมูลจาก csv อ้างอิงชื่อแต่ละ element
class ElementInfo:
    data = []

    def __init__(self):
        global elementData
        reader = csv.DictReader(open("element_info_list.csv"))
        for row in reader:
            if row["name"]:
                rowdict = {
                    "name": row["name"],
                    "column_name": row["var_name"],
                    "db_table": row["db_table"],
                }
                elementData.append(rowdict)

    def getTableAttr(self, name: str):
        for obj in elementData:
            if obj["name"] == name:
                source = [obj["column_name"], obj["db_table"]]
                query = Query(source[0], source[1]).query()
                table = Table()
                table.row.setSource(source)
                table.row.setDatarow(query)
                table.printdata()

    def checkCsv(self):
        print(elementData)

    def searchName(self, name: str, obj_list: list):
        for obj in obj_list:
            if name in obj["name"]:
                return obj

    def addDatabase(self):
        databasePath = "/Users/Maxorz/Desktop/DB_Test/ARGazqdata.db"
        global db
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName(databasePath)


class Row:
    source = []
    datarow = []

    def setSource(self, source):
        self.source = source

    def setDatarow(self, datarow):
        self.datarow = datarow


class Table:
    row = Row()

    def setTableModel(self):
        return False

    def printdata(self):
        print([self.row.source, self.row.datarow])


class Query:
    def __init__(self, column_name: str, table_name: str, condition: str):
        self.column_name = column_name
        self.table_name = table_name

    def query(self):
        condition = ""
        result = []
        # inputdata = ['table','value','row',column']
        # if self.globalTime:
        #     condition = 'WHERE time <= \'%s\'' % (self.globalTime)
        if not db.isOpen():
            db.open()
        query = QSqlQuery()
        queryString = "SELECT %s FROM %s WHERE %s IS NOT NULL LIMIT 1" % (
            self.column_name,
            self.table_name,
            self.column_name,
        )
        query.exec_(queryString)
        while query.next():
            result.append(query.value(0))
        db.close()
        return result


class Utils:
    def __init__(self):
        super().__init__()

    def unzipToFile(self, currentPath, filePath):
        fileFolderPath = currentPath + "/file"
        if not os.path.exists(fileFolderPath):
            os.makedirs(fileFolderPath)
        fileList = os.listdir(fileFolderPath)
        if len(fileList) > 0:
            for f in fileList:
                os.remove(fileFolderPath + "/" + f)
        if len(os.listdir(fileFolderPath)) == 0:
            with ZipFile(filePath, "r") as zipObj:
                zipObj.extractall(fileFolderPath)
            dbFilePath = fileFolderPath + "/azqdata.db"
            return dbFilePath

    def openConnection(self, db: QSqlDatabase):
        if db:
            if not db.isOpen():
                db.open()

    def closeConnection(self, db: QSqlDatabase):
        if db:
            if db.isOpen():
                db.close()


# todo: dynamic data query object
# class DataQuery:
#     def __inti__(self, fieldArr, tableName, conditionStr):
#         self.fieldArr = fieldArr
#         self.tableName = tableName
#         self.condition = conditionStr

#     def countField(self):
#         fieldCount = 0
#         if self.fieldArr is not None:
#             fieldCount = len(self.fieldArr)
#         return fieldCount

#     def selectFieldToQuery(self):
#         selectField = '*'
#         if self.fieldArr is not None:
#             selectField = ",".join(self.fieldArr)
#         return selectField

#     def getData(self):
#         result = dict()
#         selectField = self.selectFieldToQuery()
#         azenqosDatabase.open()
#         query = QSqlQuery()
#         queryString = 'select %s from %s' % (selectField, self.tableName)
#         query.exec_(queryString)
#         while query.next():
#             for field in range(len(self.fieldArr)):
#                 fieldName = fieldArr[field]
#                 validatedValue = self.valueValidation(query.value(field))
#                 if fieldName in result:
#                     if isinstance(result[fieldName], list):
#                         result[fieldName].append(validatedValue)
#                     else:
#                         result[fieldName] = [validatedValue]
#                 else:
#                     result[fieldName] = [validatedValue]
#         azenqosDatabase.close()
#         return result

# def valueValidation(self, value):
#     validatedValue = 0
#     if value is not None:
#         validatedValue = value
#     return validatedValue


# if __name__ == '__main__':
#     addDatabase()
#     element = ElementInfo()
#     element.checkCsv()
#     print(element.searchName('SINR\tRx[0]', elementData))
#     element.getTableAttr('SINR\tRx[0]')
# element.getTableAttr()
