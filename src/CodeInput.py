# name=big
# description=big script test
# displayinmenu=true
# displaytouser=true
# displayinselector=true
from hec.script import Plot
from hec.io import TimeSeriesContainer
from hec.io import PairedDataContainer
from hec.hecmath import TimeSeriesMath
from hec.hecmath import PairedDataMath
from hec.heclib.dss import HecDss, DSSPathname
from hec.heclib.util import HecTime
import java


def addData(dss,path,data):
  tsc = TimeSeriesContainer()
  tsc.fullName = path
  start = HecTime("01Jan2100", "1200")
  tsc.interval = 5
  rain = data
  times = []
  for value in rain :
   times.append(start. value())
   start.add(tsc.interval)
  tsc.times = times
  tsc.values = rain
  tsc.numberValues = len(rain)
  tsc.units = "MM"
  tsc.type = "PER-CUM"
  dss.put(tsc)



myDss = HecDss.open(r"C:\temp\Rainfall.dss")

addData(myDss,"/StormInjector/IFD_1/PRECIP-INC/01JAN2100/5MIN/1%AEP_10min_5090/",(24.0342,16.9658))
addData(myDss,"/StormInjector/IFD_1/PRECIP-INC/01JAN2100/5MIN/1%AEP_10min_5093/",(20.8116,20.1884))
addData(myDss,"/StormInjector/IFD_1/PRECIP-INC/01JAN2100/5MIN/1%AEP_10min_5094/", (23.8825,17.1175))
  
   
  
