# This script takes two time series and generates paired data
#
from hec.script import Plot
#from hec.io import TimeSeriesContainer
#from hec.io import PairedDataContainer
#from hec.hecmath import TimeSeriesMath
#from hec.hecmath import PairedDataMath
from hec.heclib.dss import HecDss, DSSPathname
#import java
from hec.script import Constants


dssFile = HecDss.open(r"C:\project\DSSVue-Example-Scripts\data\jreedv6.dss")
stage = dssFile.read("//test/ELEV/01Jan2000/1Hour//")
flow = dssFile.read("//test/Flow/01Jan2000/1Hour//")
paired = flow.generatePairedData(stage, Constants.FALSE)
pdc = paired.getData()
print(pdc.xunits)
print(pdc.yunits)
print(pdc.xtype)
print(pdc.ytype)
print(pdc.xparameter)
print(pdc.yparameter)
print(pdc.fullName)
print(pdc.location)
print(pdc.version)
print(pdc.numberCurves)
print(pdc.numberOrdinates)



pdc.fullName="//test/ELEV-FLOW///computed/"
dssFile.write(paired)