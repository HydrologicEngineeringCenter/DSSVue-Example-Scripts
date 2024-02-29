# Program to demonstrate writing to CWMS database using Jython
#
# Goals:
#  - start from empty TimeSeriesContainer, and put()
#  - check influence of timewindow  (writing should not be looking at time window)
#  - check influence of timezone

import DBAPI
from hec.io import TimeSeriesContainer
from hec.heclib.util import HecTime

from java.lang.reflect import Array
from java.lang import  Integer,Double


import java

def createHourlyContainer(tsid,size):
	t1 = HecTime('31Dec2009', '24:00')
	times = []
	values= []
	t=HecTime(t1)
	
	for i in range(size):
		t.addHours(1)
		times.append(t.value())
		values.append(i)
		
	tsc = TimeSeriesContainer()
	tsc.units ="cfs"
	tsc.setName(tsid)
	tsc.times = times
	tsc.values = values
	tsc.numberValues = size

	return tsc

db = DBAPI.open()
db.setOfficeId('NWDM')
tzname = db.getTimeZoneName()
print(" tzname = {}".format(tzname))
tsid = 'hectest.Flow.Inst.1Hour.0.raw'
tsc = createHourlyContainer(tsid,10)

# if timezone (of container) is set to something different than UTC/GMT - it will be shifted to GMT
#tsc.setTimeZoneID('US/Pacific')


tsc.printToConsole()
db.put(tsc)

# must set time window before using get(...)
db.setTimeWindow('31Dec2009, 24:00', '31Dec2010, 24:00')
# setting time window does not influence the db.put(...)
db.put(tsc)
flow = db.get(tsid)
flow.printToConsole()
