# name=AddTenHecMath
# displayinmenu=true
# displaytouser=true
# displayinselector=true
#  Add 10 to each value using HecMath
#
from hec.script import Plot,MessageBox
from hec.io import TimeSeriesContainer
#from hec.io import PairedDataContainer"
#from hec.io import TimeSeriesMath\n"
#from hec.io import PairedDataMath\n"
from hec.heclib.dss import HecDss,DSSPathname
import java

#  Open the file and get the data
try:  
  dssFile = HecDss.open("C:/temp/sample.dss", "10MAR2006 2400, 09APR2006 2400")
  outflow = dssFile.read("/AMERICAN/FOLSOM/FLOW-RES OUT/01JAN2006/1DAY/OBS/")
  newOutflow = outflow.add(10.)

  path = DSSPathname(newOutflow.getPath())
  fPart = path.fPart() + " + 10 HecMath"
  path.setFPart(fPart)
  newOutflow.setPathname(path.getPathname())

  dssFile.write( newOutflow)

except java.lang.Exception, e : #  Take care of any missing data or errors
  MessageBox.showError(e.getMessage(), "Error reading data")
