from hec.io import PairedDataContainer
from hec.heclib.dss import HecDss

watershed = "GREEN RIVER"
loc = "OAKVILLE"
xParam = "STAGE"
yParam = "FLOW"
date = "12Oct2003"
stages = [0.4, 0.5, 1.0, 2.0, 5.0, 10.0, 12.0]
flows = [0.1, 3, 11, 57, 235, 1150, 3700]
pdc = PairedDataContainer()
pdc.watershed = watershed
pdc.location = loc
pdc.xparameter = xParam
pdc.yparameter = yParam
pdc.version = "v1"
pdc.fullName = "/%s/%s/%s-%s///%s/" % \
	(watershed, loc, xParam, yParam, date)
pdc.xOrdinates = stages
pdc.yOrdinates = [flows]
pdc.numberCurves = 1
pdc.numberOrdinates = len(stages)
pdc.labelsUsed = False
pdc.xunits = "FEET"
pdc.yunits = "CFS"
pdc.xtype = "LOG"
pdc.ytype = "LOG"
pdc.xparameter = xParam
pdc.yparameter = yParam
pdc.date = date
pdc.transformType = 2
dssFile = HecDss.open("c:/temp/myFile.dss")
dssFile.put(pdc)
dssFile.done()
