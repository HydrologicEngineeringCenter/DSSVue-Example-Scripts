from hec.script import Plot
from hec.io import TimeSeriesCollectionContainer,TimeSeriesContainer
from hec.heclib.dss import HecDss, DSSPathname,HecTimeSeries
from hec.gfx2d import G2dDialog, DssVueSimpleDSSTimeSeriesCollection

from java.util import Vector
import sys


dss = HecTimeSeries()
tscc = TimeSeriesCollectionContainer()
tscc.fullName =R"//FOLSOM-POOL/ELEV/01JAN3000/1HOUR/C:000001|J602-C2WM-0/"
tscc.fileName = R"C:\project\DSSVue-Example-Scripts\data\Folsom_trimmed_20221129.dss"
dss.setRetrieveAllTimes(True)
istatus = dss.read(tscc, True)
print istatus
# add close parentheses after method
print tscc.size()

sts = DssVueSimpleDSSTimeSeriesCollection(tscc)

data=Vector()
data.add(sts)
plot = G2dDialog(None,"Collections test",False,data)


plot.showPlot()

x=sys.stdin.readline()