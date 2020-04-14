# name=AddTenTsc
# displayinmenu=true
# displaytouser=true
# displayinselector=true
#  Add 10 to each value using TimeSeriesContainer
#
from hec.script import *
from hec.heclib.dss import *
from hec.dataTable import *
from java import *

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

except java.lang.Exception, e :
  #  Take care of any missing data or errors
   MessageBox.showError(e.getMessage(), "Error reading data")
