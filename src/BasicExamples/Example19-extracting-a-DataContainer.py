#from hec.script import 
#from hec.hecmath import *

from hec.heclib.dss import HecDss
from hec.script import Plot, MessageBox

theFile = HecDss.open("myFile.dss")
flowDataSet = theFile.get("/Basin/loc/FLOW/01NOV2002/1Hour//")
theFile.done()

if isinstance(flowDataSet,DataContainer):
    print ('yes it is a DataContainer')


print type(flowDataSet)
flowData = flowDataSet.getData(flowDataSet)
#thisWatershed = flowData.watershed