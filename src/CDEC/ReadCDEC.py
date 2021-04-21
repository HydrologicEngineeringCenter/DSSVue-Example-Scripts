# this Script reads Oroville data (Storage,Inflow,Forebay) from CDEC
# CDEC station id is 'ORO'
#The USGS station number is 11406800
from hec.heclib.dss import HecDss
from hec.hecmath import TimeSeriesMath
from hec.plugins.cdec import CdecControlFrame
import java

def readFromCDEC(dssFileName,cdecFileName,daysBack):
  timeWindow="T-"+str(daysBack)+"D, T+1D"
  dss = HecDss.open(dssFileName,timeWindow)
  cdec = CdecControlFrame(dss)
  cdec.loadStations(cdecFileName)
  status = cdec.retrieveData()   
  print(status)

def printMath(m):
    ts=m.getData()
    print(ts.getShortName())
    print(ts.getUnits()+" "+ts.getType())
    ts.printToConsole()

fileName = R"C:\project\DSSVue-Example-Scripts\src\CDEC\Oroville.dss"
cdecName = R"C:\project\DSSVue-Example-Scripts\src\CDEC\Oroville.cdec"

daysBack = 10
#readFromCDEC(fileName,cdecName,daysBack)

dss = HecDss.open(fileName)
storage = dss.read("//OROVILLE/STORAGE//1Day/CDEC/")
inflow = dss.read("//OROVILLE/RESERVOIR INFLOW//1Day/CDEC/")

printMath(storage)
printMath(inflow)
changeInStorage = storage.successiveDifferences().divide(1.98347)
tsc = changeInStorage.getData()
tsc.units="CFS"
tsc.type=""
tsc.parameter="Change in Storage"
changeInStorage = TimeSeriesMath(tsc)
printMath(changeInStorage)

outflow = inflow.subtract(changeInStorage)
tsc = outflow.getData()
tsc.parameter="OUTFLOW"
outflow = TimeSeriesMath(tsc)
printMath(outflow)
# inflow - outflow = [change in storage]
# outflow = inflow - [change in storage] 
dss.done()
sys.stdin.readline()
