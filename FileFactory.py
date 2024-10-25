import json
import os

class FileFactory:
    #path: path to serialize array of customer
    #arrData: array of Customer
    def writeData(self,path,arrData):
        jsonString = json.dumps([item.__dict__ for item in arrData],default=str)
        jsonFile = open(path, "w")
        jsonFile.write(jsonString)
        jsonFile.close()
    #path: path to deserialize array of Customer
    #ClassName: Customer
    def readData(self,path,ClassName):
        if os.path.isfile(path) == False:
            return []
        file = open(path, "r")
        # Reading from file
        self.arrData = json.loads(file.read(), object_hook=lambda d: ClassName(**d))
        file.close()
        return self.arrData