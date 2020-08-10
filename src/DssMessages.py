#  demonstrate how to set message level
#
from hec.script import Plot, MessageBox
# from hec.io import TimeSeriesContainer
# from hec.io import PairedDataContainer
# from hec.hecmath import TimeSeriesMath
# from hec.hecmath import PairedDataMath
from hec.heclib.dss import HecDss, DSSPathname, HecDataManager
import java




#  Open the file and get the data
try:  
  dssFile = HecDss.open("C:/temp/sample.dss", "10MAR2006 2400, 09APR2006 2400")
  ###  level is the dss message level (default = 4)
	###  Highly recommended not to go below 2.  Only errors are printed with 2.
	###  0 is no messages at all (Not Recommended)
	###  1 is significant error messages (such as fatal errors)
	###  2 includes general error messages (only errors at this level)
	###  3 includes ZWRITE messages
	###  4 includes ZREAD messages (Default)
	###  7 and above are debug trace messages
	###  9 has Time Series trace
	###  10 begins file traces (real debug - not recommended)
	###  15 is maximum debug trace (Not Recommended)
  messageLevel = 10
  HecDataManager.setMessageLevel(messageLevel)  
  outflow = dssFile.read("/AMERICAN/FOLSOM/FLOW-RES OUT/01JAN2006/1DAY/OBS/")
  
  print "Done"

except java.lang.Exception, e :  #  Take care of any missing data or errors
  MessageBox.showError(e.getMessage(), "Error reading data")
  
finally: 
  print "Closing DSS File"
  dssFile.done()
