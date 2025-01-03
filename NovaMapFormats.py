import pathlib, zipfile

# NovaMap File Formats

# Exceptions:
class MissingMapNM0(Exception):
    pass
# Exception used for if an NM0 file does not contain any NM1 files
class NotValidAppendFileNM0(Exception):
    pass
# Exception used for if, when adding a file to an NM0 file, the file being added
# is not a valid NM1 or NM2 file.


# todo: neaten up comments

class nm0file(): # todo: done?
    def __init__(self, path: pathlib.Path, startLoad: bool = True):
        self.file = zipfile.ZipFile(path, mode='r')
        self.path = path
        self.tempListToSave = list()
        self.listmap = list()
        self.tempListToSaveNames = list()
        if startLoad == True:
            self.loadFiles()
    
    def loadFiles(self):
        tempB = self.file.namelist()
        self.listmap = list()
        tempC = False
        for files in tempB: 
            if files.endswith(".nm1") == True: 
                tempD = self.file.open(files, mode='r') # indexing nm1 files for use
                self.listmap.append(nm1file(tempD))
                tempC = True # stops code from raising error about no nm1 files
            elif files.endswith(".nm2") == True:
                tempE = self.file.open(files, mode='r') # above for nm2 files
                self.listmap.append(nm2file(tempE))
        if tempC == False:
            raise MissingMapNM0
    
    def addFile(self, file): # oh it works now?
        if isinstance(file, (nm1file, nm2file)) == False:
            raise NotValidAppendFileNM0
        if isinstance(file, nm1file) == True:
            nm1temp = True
        else:
            nm1temp = False
        templistA = list() # tag keys
        templistB = list() # tag values
        templistC = list() # coord X
        templistD = list() # coord Y
        temp = str() # end file
        name = file.name
        for x in file.tagList.keys():
            templistA.append(x)
        for x in file.tagList.values():
            templistB.append(x)
        for x in range(len(templistA)):
            temp = temp + (str(templistA[x]))
            temp = temp + ("=")
            temp = temp + (str(templistB[x]))
            temp = temp + ("\n")
        if nm1temp == True:
            for x in file.coordsList.keys():
                templistC.append(x)
            for x in file.coordsList.values():
                templistD.append(x)
            temp = temp + ("ENDTAGS\n")
            for x in range(len(templistC)):
                temp = temp + (str(templistC[x]))
                temp = temp + ("=")
                tempA, tempB = templistD[x]
                temp = temp + tempA
                temp = temp + ("x")
                temp = temp + tempB
                temp = temp + ("\n")
        self.tempListToSave.append(temp)
        self.tempListToSaveNames.append(name)
        
    def close(self):
        for file in self.listmap:
            file.close()
        self.file.close()
        del self

    def saveAll(self):
        finalSaveList = dict()
        temp1 = list()
        temp2 = list()
        for map in self.listmap:
            temp1.append(self.file.open(map.name).read().decode("utf-8"))
            temp2.append(map.name)
        for map in self.tempListToSave:
            temp1.append(map)
        for name in self.tempListToSaveNames:
            temp2.append(name)
        self.file = zipfile.ZipFile(self.path, mode='w')
        for name in temp2:
            ind = temp2.index(name)
            finalSaveList[name] = temp1[ind]
        for map in finalSaveList.keys():
            self.file.writestr(map, finalSaveList[map])
        self.close()

class nm1file():
    def __init__(self, file):
        self.name = file.name
        templistA = file.readlines()
        templistB = list()
        templistC = list() # tags
        templistD = list() # coords
        self.tagList = dict() # final tag plus values
        self.coordsList = dict() # final coords list
        for file in templistA:
            if type(file) == bytes: 
                templistB.append(file.decode("utf-8"))
            else: 
                templistB.append(file)
        tempA = False
        for item in templistB:
            if tempA == False and item != "ENDTAGS\n":
                templistC.append(item)
            elif item == "ENDTAGS\n":
                tempA = True
            elif tempA == True:
                templistD.append(item)
        for item in templistC:
            tempB = item.strip()
            tempC, tempD = tempB.split('=')
            self.tagList[tempC] = tempD
        for item in templistD:
            tempB = item.strip()
            print(item)
            tempC, tempD = tempB.split('=')
            tempE, tempF = tempD.split('x')
            self.coordsList[tempC] = (tempE, tempF)  

    def close(self):
        del self

class nm2file():
    def __init__(self, file):
        self.name = file.name
        templistA = file.readlines()
        templistB = list()
        self.tagList = dict() # final tag plus values
        for file in templistA:
            if type(file) == bytes: 
                templistB.append(file.decode("utf-8"))
            else: 
                templistB.append(file)
        for item in templistB:
            tempA = item.strip()
            tempB, tempC = str(tempA).split('=')
            self.tagList[tempB] = tempC
    def close(self):
        del self
            
def createnm0(name: str, files: list): # sure enough, this was never the problem
    name = (name + ".nm0")
    zipfile.ZipFile(name, 'x')
    path = pathlib.Path("./" + name)
    nm0 = nm0file(path, False)
    y = False
    for x in files:
        try: nm0.addFile(x)
        except NotValidAppendFileNM0: y = True
    if y == True: raise NotValidAppendFileNM0
    nm0.saveAll()
    nm0 = nm0file(path, True)
    return nm0

def createnm1(name: str, tags: dict, coords: dict):
    name = (name + ".nm1")
    file = open(name, 'x')
    templistA = list() # tag keys
    templistB = list() # tag values
    templistC = list() # coord names
    templistD = list() # coord X
    templistE = list() # coord Y
    for x in tags.keys():
        templistA.append(x)
    for x in tags.values():
        templistB.append(x)
    for x in coords.keys():
        templistC.append(x)
    for x in coords.values():
        templistD.append(x[0])
        templistE.append(x[1])
    for x in range(len(templistA)):
        file.write(str(templistA[x]))
        file.write("=")
        file.write(str(templistB[x]))
        file.write("\n")
    file.write("ENDTAGS\n")
    for x in range(len(templistC)):
        file.write(str(templistC[x]))
        file.write("=")
        file.write(str(templistD[x]))
        file.write("x")
        file.write(str(templistE[x]))
        file.write("\n")
    return file

def createnm2(name: str, tags: dict):
    name = (name + ".nm2")
    file = open(name, 'x')
    templistA = list() # tag keys
    templistB = list() # tag values
    for x in tags.keys():
        templistA.append(x)
    for x in tags.values():
        templistB.append(x)
    for x in range(len(templistA)):
        file.write(str(templistA[x]))
        file.write("=")
        file.write(str(templistB[x]))
        file.write("\n")
    return file
