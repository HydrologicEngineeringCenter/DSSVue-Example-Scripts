#  Add 10 to each value using HecMath
#
from hec.script import Plot, MessageBox
# from hec.io import TimeSeriesContainer
# from hec.io import PairedDataContainer
# from hec.hecmath import TimeSeriesMath
# from hec.hecmath import PairedDataMath
from hec.heclib.dss import HecDss, DSSPathname
import java
import sys



#  Open the file and get the data
try:  
  dssFile = HecDss.open(sys.argv[1] + "\\sample.dss", "10MAR2006 2400, 09APR2006 2400")
  outflow = dssFile.read("/AMERICAN/FOLSOM/FLOW-RES OUT/01JAN2006/1DAY/OBS/")
  newOutflow = outflow.add(10.)

  path = DSSPathname(newOutflow.getPath())
  fPart = path.fPart() + " + 10 HecMath"
  path.setFPart(fPart)
  newOutflow.setPathname(path.getPathname())

  dssFile.write(newOutflow)
  
  print "Done"

except java.lang.Exception, e :  #  Take care of any missing data or errors
  MessageBox.showError(e.getMessage(), "Error reading data")
  
finally:
  print "Closing DSS File"
  dssFile.done()
