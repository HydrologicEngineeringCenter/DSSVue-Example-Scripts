from hec.heclib.dss import HecDss, DSSPathname, HecDSSUtilities
from hec.heclib.util import HecTime, Heclib
import sys
import os, time


def getDssFiles(dir):
 rval=[]
 
 dssFileNames = os.listdir(dir)
 for f in dssFileNames:
    if f.endswith(".dss"):
        fn = dir+f
        rval.append(fn)
 return rval

dir = "c:/temp/a/"
files = getDssFiles(dir)
Heclib.zset("MLVL", "", 0) 
outputFileName = R"c:\temp\result6.dss"
if os.path.exists(outputFileName):
  os.remove(outputFileName)
HecDss.open(outputFileName,6)
for f in files:
    print("processing. "+f)
    start = time.time()
    dss = HecDSSUtilities()
    dss.setDSSFileName(f)
    dss.copyFile(outputFileName)
    dss.done()
    end = time.time()
    print(end-start)

print("done.")
print ("press enter to exit.")
a = input()
