# from hec.script import Plot, MessageBox
# from hec.io import TimeSeriesContainer
from hec.heclib.dss import HecDss, DSSPathname, HecDSSUtilities
from hec.heclib.util import HecTime
#import java
import sys
#import glob,os
import os


def getDssFiles(dir):
 rval=[]
 
 dssFileNames = os.listdir(dir)
 for f in dssFileNames:
    if f.endswith(".dss"):
        fn = dir+f
        rval.append(fn)
 return rval

dir = "c:/temp/"
files = getDssFiles(dir)
outputFileName = R"c:\temp\result.dss"
for f in files:
    print("processing. "+f)
    dss = HecDSSUtilities()
    dss.setDSSFileName(f)
    dss.copyFile(outputFileName)
    dss.done()

print("done.")
print ("press enter to exit.")
a = input()
