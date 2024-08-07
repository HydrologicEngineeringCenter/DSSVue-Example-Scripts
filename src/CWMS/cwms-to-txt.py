# this script exports from CWMS into 
# a text file that can be imported by OpenDCS

from hec.heclib.dss import HecDss, DSSPathname
from hec.heclib.util import HecTime
import datetime
import array

import DBAPI, sys


def write_to_opendcs_text_file(tsc, filename):
	with open(filename, 'w') as f:
        f.write("SET:TZ=UTC\n")
        f.write("SET:UNITS="+tsc.getUnits()+"\n")
        f.write("TSID:"+tsc.getFullName()+"\n")

		for i in range(len(tsc.times)):
            t = HecTime(tsc.times[i],HecTime.MINUTE_GRANULARITY)      
            s = "{:04d}/{:02d}/{:02d}-{:02d}:{:02d},{:f},{:d}\n".format(t.year(), t.month(), t.day(), t.hour(), t.minute(),tsc.values[i],tsc.quality[i])
            f.write(s)


startTime  =  "08Aug2020  0000"
endTime    = "08Aug2022  0000"

db = DBAPI.open()
#tsid = 'FTPK-Lower-D063,0m.Temp-Water.Inst.1Day.0.Rev-NWO-Evap'
tsid = 'FTPK-Lower-D010,0m.Temp-Water.Inst.1Day.0.Rev-NWO-Evap'


db.setTimeZone("UTC")
db.setTimeWindow(startTime, endTime)
ts   = db.get(tsid)
ts.printToConsole()
filename = "c:/tmp/"+tsid+".txt"
write_to_opendcs_text_file(ts,filename)
#print(ts.times[0])
#print(ts.quality[0])
print("done")


#SET:TZ=UTC
#SET:UNITS=in
#TSID:testsite-pattern.Precip-Cum.Inst.1Hour.0.test
#2024/06/13-11:00,1,0
#2024/06/13-12:00,2,0
#2024/06/13-13:00,3,0
#2024/06/13-14:00,4,0
#2024/06/13-15:00,5,0
 