#  Add 10 to each value using TimeSeriesContainer
#
from hec.script import Plot, MessageBox
# from hec.io import TimeSeriesContainer
# from hec.io import PairedDataContainer
# from hec.hecmath import TimeSeriesMath
# from hec.hecmath import PairedDataMath
from hec.heclib.dss import HecDss, DSSPathname
import java


#  Open the file and get the data
try:  
  dssFile = HecDss.open("C:/temp/sample.dss", "10MAR2006 2400, 09APR2006 2400")
  outflow = dssFile.get("/AMERICAN/FOLSOM/FLOW-RES OUT/01JAN2006/1DAY/OBS/")
  i = 0
  for value in outflow.values :
    outflow.values[i] += 10.
    i += 1

  path = DSSPathname(outflow.fullName)
  fPart = path.fPart() + " + 10"
  path.setFPart(fPart)
  outflow.fullName = path.getPathname()

  dssFile.put(outflow)
  print "Done"

except java.lang.Exception, e :
  #  Take care of any missing data or errors
   MessageBox.showError(e.getMessage(), "Error reading data")
   
finally:
  print "Closing DSS File"
  dssFile.done()
