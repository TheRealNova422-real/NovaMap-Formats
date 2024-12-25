import pathlib, zipfile

# NovaMap Formats, written entirely by Nova422 (The One And Only)
# Do not pass off, or attempt to pass off any of my code as your own
#
# NovaMap files are intended to be a quick and easy solution to storing locations
# of objects and other locations within 2D space.
#
# NM0 (En-Em-Zero) files are folders using zip compression to house the full map.
#
# NM1 (En-Em-One) files are positional maps. They contain a set of metadata,
# intended to be used by the end user to give additional information to the location
# defined by the file.
# The metadata begins with the name of the location, followed by a resolution and 
# scale. Resolution refers to the full size of the map defined by the smallest unit
# of measurement used to define an object's location.
# Scale is an optional string which defines the relationship between resolution and
# size. A scale of 1 meter and resolution of 100x100, as an example, will result
# in a map of 100 meters by 100 meters.
# The metadata may also contain other optional details for use by the end user.
#
# NM2 (En-Em-Two) files are similar to NM1 files, but are simply objects rather than
# full locational maps. They may be used interchangably within an NM1, without the
# requirement of being a map.
#
# NM1 files may call other NM1 files, however they may not loop;
# NM1 file A may call NM1 file B, but if that is so, NM1 file B may not call NM1 file A
# and will raise an exception. This exception will be ignored if, within the metadata,
# it contains the tag NonEuclidean = True. 
# Presently, built in compatibility with non-Euclidean geometry is planned, however
# I (Nova) have absolutely zero clue how to develop it. Perhaps it will be revealed
# to me in a dream. Until then, I leave it to you to attempt it, and wish you luck.
#
# An example of these files is as follows:
# MainMap.nm0
#-> House.nm1       - calls LivingRoom.nm1 and Kitchen.nm1
#   LivingRoom.nm1  - calls Sofa.nm2
#   Kitchen.nm1     - calls Fridge.nm2
#   Sofa.nm2        - has "Sittable" tag
#   Fridge.nm2      - has "Container" tag
#

# Exceptions:
class MissingMapNM0(Exception):
    pass
# Exception used for if an NM0 file does not contain any NM1 files
class RecursiveNM1(Exception):
    pass
# Exception used for if two NM1 files call each other, and the non-Euclidean tag
# is not present

# incomplete
class nm0file():
    def __init__(self, path):
        path = pathlib.Path(path)
        temp = zipfile.ZipFile(path, mode='r')
        self.file = temp
        tempB = self.file.namelist()
        tempC = False 
        for files in tempB:
            if files.find(".nm1") == -1:
                tempC = True
            else: pass
        if tempC == True: raise MissingMapNM0
        self.listobj = list()

    def callNM1(self, NM1):
        tempD = self.file.open(NM1, mode='w')
        self.listobj.append(nm1file(tempD))
    
    def close(self):
        self.file.close()
        del self
        # Closes the selected NM0 and deletes the object that called it

class nm1file():
    def __init__(self, file):
        pass

temp = zipfile.ZipFile('c.zip', mode='r')

tempb = temp.namelist()
tempc = False
for files in tempb:
    if files.find("nm1") == -1:
        tempc = True
    else: pass
if tempc == True: raise MissingMapNM0

mainfile = nm0file('c.zip')
