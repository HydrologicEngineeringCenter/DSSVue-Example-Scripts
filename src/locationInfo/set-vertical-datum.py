from hec.script import Plot
from hec.heclib.dss import HecDss, DSSPathname
from hec.heclib.util import HecTime
from hec.io import TimeSeriesContainer
import os

path = "//Flowing River/Flow//1Day/test/"

def createTSC():
    
    tsc=TimeSeriesContainer()
    tsc.fullName=path
    tsc.values=[1,2,3]
    t = HecTime("17Mar1975")
    tsc.times=[t.value(),t.value()+1440,t.value()+2*1440]
    tsc.numberValues=3
    tsc.timeZoneID="America/Santiago"
    return tsc

def printTSC(c):
    print("verticalDatum: "+str(c.verticalDatum))
    print("verticalUnits:"+str(c.verticalUnits))
    print("locationTimezone:"+tsc.locationTimezone)
    print("timeZoneID:"+tsc.timeZoneID)
    c.printToConsole()



fn =r"c:/tmp/lat-long-test.dss"
os.remove(fn)
dss = HecDss.open(fn)
tsc = createTSC()

dss.put(tsc)
tsc2 = dss.get(path)
printTSC(tsc2)

# set lat/lon and vertical datum
tsc = createTSC()
tsc.setLatLong(123.45,67.89)
tsc.verticalDatum = 1
tsc.verticalUnits =1  # 1=feet, 2=meters
dss.put(tsc)
tsc2 = dss.get(path)
printTSC(tsc2)

# note: the following lat/long verticalDatum, and verticalUnits will not save
# because it is location information, potentially shared by other datasets
tsc = createTSC()
tsc.setLatLong(-123.45,-67.89)
tsc.verticalDatum = 2
tsc.verticalUnits = 2  # 1=feet, 2=meters
dss.put(tsc)
tsc2 = dss.get(path)
printTSC(tsc2)


 

