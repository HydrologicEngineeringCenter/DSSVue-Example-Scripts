# change timeseries data from 5 minute to 15 minute interval

from hec.heclib.dss import HecDss
from hec.hecmath import TimeSeriesMath
from java.util import Vector

fileName = R"C:\project\DSSVue-Example-Scripts\data\5minute.dss"
path ="/time-series////5Minute//"
print("filename: "+fileName)
dss = HecDss.open(fileName)
tsc = dss.get(path)
tsc.printToConsole()
tsm = TimeSeriesMath(tsc)
# transformTimeSeries(string timeInterval, string timeOffset, string functionType)
# where functionType is : 
# "INT" for linear interpolation
# "AVE" for period average over interval
# "ACC" for accumulation over interval
ts_15min = tsm.transformTimeSeries("15Min","0Minutes","INT").getContainer()
ts_15min.printToConsole()

# alternate method that uses dataType to determine function type argument
#interpolateDataAtRegularInterval(timeInterval, timeOffset) 