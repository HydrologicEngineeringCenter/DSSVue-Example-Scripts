# name=WriteDss
# displayinmenu=true
# displaytouser=true
# displayinselector=true
from hec.script import *
from hec.heclib.dss import *
from hec.heclib.util import *
from hec.io import *
import java

try : 
  try :
    myDss = HecDss.open("C:/temp/test.dss")
    tsc = TimeSeriesContainer()
    tsc.fullName = "/BASIN/LOC/FLOW//1HOUR/OBS/"
    start = HecTime("04Sep1996", "1330")
    tsc.interval = 60
    flows = [0.0,2.0,1.0,4.0,3.0,6.0,5.0,8.0,7.0,9.0]   
    times = []
    for value in flows :
      times.append(start.value())
      start.add(tsc.interval)
    tsc.times = times
    tsc.values = flows
    tsc.numberValues = len(flows)
    tsc.units = "CFS"
    tsc.type = "PER-AVER"
    myDss.put(tsc)
    
  except Exception, e :
    MessageBox.showError(' '.join(e.args), "Python Error")
  except java.lang.Exception, e :
    MessageBox.showError(e.getMessage(), "Error")
finally :
  myDss.close()
