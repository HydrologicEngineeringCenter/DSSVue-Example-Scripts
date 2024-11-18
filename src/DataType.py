from hec.heclib.dss import HecDss, DSSPathname


def deleteRecords(dss,pathname):
	""" find all records that match pathname (removing D part) and delete from the DSS file""" 
	path = getPathWithNewDPart(pathname,"*")
	paths = dss.getCatalogedPathnames(path)
	delete_list = []
	for p in paths:
		delete_list.append(p)
		print(p)
		
	dss.delete(delete_list)
		

def getPathWithNewDPart(pathname,newDpart):
	dp = DSSPathname(pathname)
	return DSSPathname.buildPathnameFromParts(dp.aPart(),dp.bPart(),dp.cPart(),newDpart,dp.ePart(),dp.fPart())
	

def rewriteTimeSeriesAsDouble(dss,pathname):
	""" converts time series to double-precision 
	     convert by:
	       - reading the time-series into memory (drop D part from path)
	       - delete records from disk
	       - save to disk with storedAsdoubles = True     
	"""
		
	path = getPathWithNewDPart(pathname,"")
	tsc = dss.get(path,True)
	print("tsc.dataType =",tsc.dataType)
	if tsc.storedAsdoubles:
		print("already doubles")
		return
	deleteRecords(dss,path)
	
	tsc.storedAsdoubles = True
	tsc.setFullName(path)
	dss.put(tsc)
	print("converted/saved to double")


fileName = r"C:\tmp\forecast7a.dss"
#path1 = "//FTPK/FLOW-LOCAL/01Jan2024/1DAY/FCST RUNOFF: ----40/"
path = "//Fort Peck Lake-UNIT 1/FLOW/01Jan2024/1DAY/Lookback/"

dss = HecDss.open(fileName)
rewriteTimeSeriesAsDouble(dss,path)



print("all done.")


