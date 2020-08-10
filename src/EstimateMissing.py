#  Fill in missing values using HecMath
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
  flow = dssFile.read("/AMERICAN/FOLSOM/FLOW-RES IN/01JAN2006/1DAY/OBS/")

  newflow = flow.estimateForMissingValues(10)

  path = DSSPathname(newflow.getPath())
  fPart = path.fPart() + " + FILLED"
  path.setFPart(fPart)
  newflow.setPathname(path.getPathname())

  dssFile.write( newflow)
  print "Done"

except java.lang.Exception, e :
  #  Take care of any missing data or errors
   MessageBox.showError(e.getMessage(), "Error reading data")

finally:
  print "Closing DSS File"
  dssFile.close()
    