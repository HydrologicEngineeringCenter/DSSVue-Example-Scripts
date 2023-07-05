# rename F part to match convention

#OLD:  /RUSSIANNAPA/APCC1/FLOW/01MAR2017/1HOUR/C:000035|T:0572017/
#                                              012345678901234
#  057 -- is day 57 in year 2017
#
#NEW:  /RUSSIANNAPA/APCC1/FLOW/01MAR2017/1HOUR/C:000035|T:YYYYMMdd-hhmm/

from hec.heclib.dss import HecDss, DSSPathname,HecDSSUtilities
from java.time import LocalDateTime
from java.time.temporal import ChronoUnit
from java.time.format import DateTimeFormatter
from java.util import Vector

fileName = R"C:\tmp\ensemble_for_beth1.dss"
print("filename: "+fileName)
dss = HecDss.open(fileName)
paths = dss.getPathnameList()
u = HecDSSUtilities()
u.setDSSFileName(fileName)
pathnameList=Vector()
newPathnameList=Vector()
for p in paths:
  dp = DSSPathname(p)
  f = dp.fPart()
  yr = int(f[14:18])
  julian = int(f[11:14]) 
  t = LocalDateTime.of(yr, 1, 1, 0, 0)
  t = t.plus(julian-1, ChronoUnit.DAYS)
  
  #	YYYYMMDD-hhmm/RUSSIANNAPA/APCC1/FLOW/01DEC2016/1HOUR/C:000001|T:201612355-1200/
  fmt = DateTimeFormatter.ofPattern("YYYYMMdd-hhmm")
  newFpart = f[0:11]+t.format(fmt)
#  print(f,julian,yr,t.toString(),newFpart)
  dp.setFPart(newFpart)
#  print(dp.toString())
  pathnameList.add(p)
  newPathnameList.add(dp.toString())
#  print(pathnameList)
dss.done()
u.renameRecords(pathnameList,newPathnameList)