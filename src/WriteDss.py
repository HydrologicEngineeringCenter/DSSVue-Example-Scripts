#Make TimeSeriesContainer, add values and times, then put
from hec.script import Plot, MessageBox
from hec.io import TimeSeriesContainer
# from hec.io import PairedDataContainer
# from hec.hecmath import TimeSeriesMath
# from hec.hecmath import PairedDataMath
from hec.heclib.dss import HecDss, DSSPathname
from hec.heclib.util import HecTime
import java
import sys

try:
  myDss = HecDss.open(sys.argv[1] + "\\test.dss")
  tsc = TimeSeriesContainer()
  tsc.fullName = "/BASIN/LOC/FLOW//1HOUR/OBS/"
  start = HecTime("04Sep1996", "1330")
  tsc.interval = 60
  flows = [0.0,2.0,1.0,4.0,3.0,6.0,5.0,8.0,7.0,9.0]   
  times = []
  for value in flows:
    times.append(start.value())
    start.add(tsc.interval)
  tsc.times = times
  tsc.values = flows
  tsc.numberValues = len(flows)
  tsc.units = "CFS"
  tsc.type = "PER-AVER"
  myDss.put(tsc)
  print "Done"
except Exception, e:
  print(e)
finally:
  print "Closing DSS File"
  myDss.close()
