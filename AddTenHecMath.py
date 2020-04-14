# name=AddTenHecMath
# displayinmenu=true
# displaytouser=true
# displayinselector=true
#  Add 10 to each value using HecMath
#
from hec.script import *
from hec.hecmath import *
from java import *

#  Open the file and get the data
try:  
  dssFile = DSS.open("C:/temp/sample.dss", "10MAR2006 2400, 09APR2006 2400")
  outflow = dssFile.read("/AMERICAN/FOLSOM/FLOW-RES OUT/01JAN2006/1DAY/OBS/")
  newOutflow = outflow.add(10.)

  path = DSSPathname(newOutflow.getPath())
  fPart = path.fPart() + " + 10 HecMath"
  path.setFPart(fPart)
  newOutflow.setPathname(path.getPathname())

  dssFile.write( newOutflow)

except java.lang.Exception, e :
  #  Take care of any missing data or errors
   MessageBox.showError(e.getMessage(), "Error reading data")
