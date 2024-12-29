import pathlib, zipfile

# NovaMap File Formats

# NovaMap files are intended to be a quick and easy solution to storing locations
# of objects and other locations within 2D space.

# NM0 (En-Em-Zero) files are folders using zip compression to house the full map.

# NM1 (En-Em-One) files are positional maps. They contain a set of metadata,
# followed by a list of coordinates.

# NM2 (En-Em-Two) files are references. Similar to NM1s, they contain a set of
# metadata tags but without any coordinate sets.

# Metadata is stored in the form of Tags, which are accessed by the program and
# can be accessed at any time.

# NM1 and NM2 files begin with the tags, 

# An example of these files is as follows:
# MainMap.nm0
# -> House.nm1       - calls LivingRoom.nm1 and Kitchen.nm1
#   LivingRoom.nm1  - calls Sofa.nm2
#   Kitchen.nm1     - calls Fridge.nm2
#   Sofa.nm2        - has "Sittable" tag
#   Fridge.nm2      - has "Container" tag


# Exceptions:
class MissingMapNM0(Exception):
    pass
# Exception used for if an NM0 file does not contain any NM1 files
class RecursiveNM1(Exception):
    pass
# Exception used for if two NM1 files call each other, and the non-Euclidean tag
# is not present

# todo: nm1 nm2 plus tags

class nm0file(): # almost complete, just debugging
    def __init__(self, path):
        path = pathlib.Path(path) # pathlib Path object defines what file is opened
        temp = zipfile.ZipFile(path, mode='r') # how the file is read
        self.file = zipfile.ZipFile(path, mode='r') # saving for later
        tempB = self.file.namelist() # am i really going to comment every little thing?
        self.listmap = list() # list of all the nm1 and nm2 objects (yes, yes i am)
        tempC = False # for exception handling
        for files in tempB:
            print(files)
            if files.endswith(".nm1") == True: 
                tempD = temp.open(files, mode='r') # indexing nm1 files for use later
                print(tempD)
                print(tempD.readlines())
                tempY = tempD.readlines()
                print(type(tempY))
                print("A")
                self.listmap.append(nm1file(tempD))
                tempC = True # stops code from raising error about no nm1 files
            elif files.endswith(".nm2") == True:
                tempE = temp.open(files, mode='r') # above for nm2 files
                self.listmap.append(nm2file(tempE))
        if tempC == False:
            raise MissingMapNM0
    def close(self):
        for file in self.listmap():
            file.close()
        self.file.close()
        del self
        # Closes the selected NM0 and deletes the object that called it

class nm1file():
    def __init__(self, file):
        templist = file.readlines()
        print(templist)
        templistA = list() # tags
        templistB = list() # coords
        self.tagList = dict() # final tag plus values
        self.coordsList = dict() # final coords list
        tempA = False
        for item in templist:
            if tempA == False and item != "ENDTAGS\n":
                templistA.append(item)
            elif item == "ENDTAGS\n":
                tempA = True
            elif tempA == True:
                templistB.append(item)
        for item in templistA:
            tempB = item.strip()
            print(tempB)
            tempC, tempD = tempB.split('=')
            self.tagList[tempC] = tempD # code is very very much haunted
        for item in templistB:
            tempB = item.strip()
            print("AA")
            print(tempB)
            tempC, tempD = tempB.split('x')
            self.coordsList[tempC] = tempD   
        print(self.tagList)
        print(self.coordsList) 
    def close(self):
        del self

class nm2file():
    def __init__(self, file):
        print("X")
        templist = file.readlines()
        self.tagList = dict() # final tag plus values
        for item in templist:
            tempA = item.strip()
            tempB, tempC = str(tempA).split('=')
            print(tempB)
            print(tempC)
            self.tagList.update({tempB, tempC})
    
    def close(self):
        del self
            

bwa = open("mapTest.nm1")
# print(bwa)
# bw2 = nm1file(bwa)
mainfile = nm0file('i.zip')
