# -*- coding: utf-8 -*-
from hec.heclib.util import HecTime
from hec.heclib.dss import HecDss, DSSPathname
from hec.io import TimeSeriesContainer
from hec.heclib.util import HecTime
import java
import sys
import os
fileName = "c:/temp/day_granularity.dss"   
if os.path.isfile(fileName):
  os.remove(fileName)

dss = HecDss.open(fileName)

tsc = TimeSeriesContainer()
tsc.fullName = "/test/day_granularity/FLOW/04Sep3000/1YEAR/MODEL/"


tsc.values = range(1,3000,1)
start = HecTime("04Sep3000", "1330")
LastYear = 3000
AnnualTimes = []
for x in range(len(tsc.values)) :
 LastYear += 1
 hecTime = HecTime('31Dec%04d 2400' % LastYear, HecTime.DAY_GRANULARITY)
 AnnualTimes.append(hecTime.value())

tsc.times = AnnualTimes
tsc.numberValues = len(tsc.values)
tsc.units = "CFS"
tsc.type = "PER-AVER"
tsc.setTimeGranularitySeconds(86400)
dss.put(tsc) 