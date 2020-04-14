# name=EstimateMissing
# displayinmenu=true
# displaytouser=true
# displayinselector=true
#  Fill in missing values using HecMath
#
from hec.script import *
from hec.hecmath import *
from java import *

#  Open the file and get the data
try:  
  dssFile = DSS.open("C:/temp/sample.dss", "10MAR2006 2400, 09APR2006 2400")
  flow = dssFile.read("/AMERICAN/FOLSOM/FLOW-RES IN/01JAN2006/1DAY/OBS/")

  newflow = flow.estimateForMissingValues(10)

  path = DSSPathname(newflow.getPath())
  fPart = path.fPart() + " + FILLED"
  path.setFPart(fPart)
  newflow.setPathname(path.getPathname())

  dssFile.write( newflow)

except java.lang.Exception, e :
  #  Take care of any missing data or errors
   MessageBox.showError(e.getMessage(), "Error reading data")
