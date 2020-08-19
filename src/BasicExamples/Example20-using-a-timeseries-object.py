from hec.heclib.dss import HecDss, HecTimeSeries
from hec.io import TimeSeriesContainer
from hec.heclib.util import HecTime

watershed = "Green River"
loc = "OAKVILLE"
param = "STAGE"
ver = "OBS"
startTime = "12Oct2003 0100"
values = [12.36, 12.37, 12.42, 12.55, 12.51, 12.47, 12.43, 12.39]
hecTime = HecTime()

tsc = TimeSeriesContainer()
tsc.watershed = watershed
tsc.location = loc
tsc.parameter = param
tsc.version = ver
tsc.fullName = "/%s/%s/%s//1HOUR/%s/" % (watershed, loc, param, ver)
tsc.interval = 60

hecTime.set(startTime)
times=[]

for value in values:
    times.append(hecTime.value())
    hecTime.add(tsc.interval)

tsc.values = values
tsc.times = times
tsc.startTime = times[0]
tsc.endTime = times[-1]

tsc.numberValues = len(values)
tsc.units = "FEET"
tsc.type = "INST-VAL"
dssFile = HecDss.open("myFile.dss")
dssFile.put(tsc)
dssFile.done()