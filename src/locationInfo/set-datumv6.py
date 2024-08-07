from hec.script import Plot
from hec.heclib.dss import HecDss, DSSPathname
from hec.heclib.util import HecTime
from hec.io import TimeSeriesContainer
import os

path = "/CHILE/1010007/PRECIP-INC/01JAN2009/1DAY/KARL/"

def String(o):
    if o is None:
      return ""
    return str(o)

def printTSC(c):
    
    print("verticalDatum: "+String(c.verticalDatum))
    print("verticalUnits:"+String(c.verticalUnits))
    print("locationTimezone:"+String(tsc.locationTimezone))
    print("timeZoneID:"+String(tsc.timeZoneID))
    c.printToConsole()



fn =R"C:\project\DSSVue-Example-Scripts\src\locationInfo\test-vert.dss"
dss = HecDss.open(fn)
tsc = dss.get(path)
printTSC(tsc)

1/0
# set lat/lon and vertical datum
tsc.setLatLong(123.45,67.89)
tsc.verticalDatum = 1
tsc.verticalUnits =1  # 1=feet, 2=meters
dss.put(tsc)
tsc2 = dss.get(path)
printTSC(tsc2)



 

