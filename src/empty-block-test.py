from hec.script import Constants
from hec.io import TimeSeriesContainer
from hec.heclib.dss import HecDss, HecDSSUtilities
from hec.heclib.util import HecTime

filename = "C:/tmp/a.dss"
dss = HecDss.open(filename)

def allMissing(pathname):
	"""
	return true if all data is missing in the pathname (time-series)
	"""
	tsc = dss.get(pathname)
	return tsc.allMissing()


def createOneYear(year, missing):
	"""
	Creates one year of time-series data,  if missing is True then create a year of missing data
	"""
	tsc = TimeSeriesContainer()
	tsc.fullName = "//empty-blocks/flow//1Day//"
	t = HecTime()
	t.setYearMonthDay(year,1,1)
	tsc.numberValues = 365
	tsc.setStartTime(t)
	if missing:
		tsc.values = [Constants.UNDEFINED for i in range(tsc.numberValues)  ]
	else:
		tsc.values = [i**2 for i in range(tsc.numberValues)  ]
	tsc.units = "cfs"
	dss.put(tsc)

# create five years of data
for year in (2001,2002,2003,2004,2005):
	createOneYear(year,False)

# create file years of missing data
for year in (2006,2007,2008,2009,2010):
	createOneYear(year,True)


path = "//empty-blocks/flow/01Jan2010/1Day//"
dssUtility = HecDSSUtilities()
dssUtility.setDSSFileName(filename)
# if all data is mising in this path remove it.
if allMissing(path):
	dssUtility.delete([path])


dssUtility.close()
dss.close()
