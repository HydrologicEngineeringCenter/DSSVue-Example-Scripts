from hec.heclib.dss import HecDss, DSSPathname

def rewriteTscAsDouble(dss,pathname):
	""" converts time series record to double-precision 
	     convert by:
	       - reading the record into memory
	       - delete from disk
	       - save to disk with storedAsdoubles = True     
	"""

	if dss.recordExists(pathname):
		tsc = dss.get(pathname)
		print("tsc.dataType =",tsc.dataType)
		if tsc.storedAsdoubles:
			print("already doubles")
			return
		d = [pathname]
		dss.delete(d)
		tsc.storedAsdoubles = True
		dss.put(tsc)
		print("converted/saved to double")
	else:
		print(path,"does not exist")


fileName = r"C:\tmp\forecast7.dss"
path = "//FTPK/FLOW-LOCAL/01Jan2024/1DAY/FCST RUNOFF: ----40/"
#path = "//FTPK/ELEV-ESTIMATED/01Jan2024/IR-Month/BEST-MRBWM/"

dss = HecDss.open(fileName)
rewriteTscAsDouble(dss,pathname)
