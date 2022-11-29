from hec.heclib.dss import HecDss, HecTimeSeries
from hec.io import TimeSeriesContainer
import sys


file = R"C:\project\DSSVue-Example-Scripts\data\Osageroutedflow11-29-22b.dss"

path="//BAGL/FLOW-OUT//1HOUR/FCST-NWK-ROUTED/"

t1="12Nov 2022 12:00"
t2="14Nov 2022 24:00"

dss = HecDss.open(file)
dss.setTrimMissing(True)
print("dss.getTrimMissing()",dss.getTrimMissing())
flow = dss.get(path,t1,t2)
print("using get:  len(flow.values) = ",len(flow.values))
flow = dss.read(path,t1,t2).getData()
print("using read:  len(flow.values) = ",len(flow.values))

dss.setTrimMissing(False)
print("dss.getTrimMissing()",dss.getTrimMissing())
flow = dss.get(path,t1,t2)
print("using get:  len(flow.values) = ",len(flow.values))
flow = dss.read(path,t1,t2).getData()
print("using read:  len(flow.values) = ",len(flow.values))


sys.stdin.readline()

#  --- results ---
##('dss.getTrimMissing()', True)
##('using get:  len(flow.values) = ', 733)
##('using read:  len(flow.values) = ', 49)
##
##('dss.getTrimMissing()', False)
##('using get:  len(flow.values) = ', 733)
#('using read:  len(flow.values) = ', 61)