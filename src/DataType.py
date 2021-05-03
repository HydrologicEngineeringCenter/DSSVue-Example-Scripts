from hec.heclib.dss import HecDss, HecTimeSeries
from hec.io import TimeSeriesContainer
import sys


file = R"C:\project\DSSVue-Example-Scripts\data\kinzua.dss"
path="//AG RESORT/FLOW/01Feb2014/15Minute/FOR:ALTERNATIVE 1:B0C0/"

# tsc =TimeSeriesContainer()
# tsc.fullName = path
# dss =HecTimeSeries(file)
# status = dss.read(tsc, True)
# print("precision:",tsc.precision)
# print(dss.getRecordInfo(path).recordType)
# print (tsc.type)
# -------------------
dss2 = HecDss.open(file)
flow = dss2.get(path)
print (flow.numberValues )
print("flow.dataType =",flow.dataType)




sys.stdin.readline()
