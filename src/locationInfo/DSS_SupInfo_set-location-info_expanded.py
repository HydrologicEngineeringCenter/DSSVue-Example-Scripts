#from hec.script import Plot
from hec.heclib.dss import HecDss, DSSPathname
import csv
 
class csvfile:

  def __init__(self, filename):
    raw=list(csv.reader(open(filename)))
    self.column_names =raw[0] 
    self.data = raw[1:]
    print(self.column_names)
    # print(self.data)

  def getString(self,rowIndex,column_name):
    colIndex = self.column_names.index(column_name)
    print(colIndex, column_name, pathname)
    return self.data[rowIndex][colIndex]

  def getFloat(self,rowIndex,column_name):
    s = self.getString(rowIndex,column_name)
    return float(s)

  def getInt(self,rowIndex,column_name):
    s = self.getString(rowIndex,column_name)
    return int(s)

  def size(self):
    return len(self.data)

# begin main program
# note: location info can be created when saving a specific timeseriescontainer
# however, location info can't be modified as part of a timeseries container
# because that location info is potentially  shared with other containers

csv = csvfile(r"D:/temp/DSS_SupInfo_location.csv")
fn =r"C:/ProgramFiles/HEC/CWMS/CWMS_v3.2.3/CWMS-v3.2.3/common/grid/Chile/Chile_America_Santiago_SI.dss"
dss = HecDss.open(fn)

for i in range(0,csv.size()):
  pathname = csv.getString(i,"\xef\xbb\xbfpathname")
  # print(pathname)
  dssPath = DSSPathname(pathname)
  dssPath.setDPart("") # remove dates from pathname
  tsc=dss.get(dssPath.pathname())

  tsc.setLatLong(csv.getFloat(i,"y"),csv.getFloat(i,"x"))

  tsc.horizontalDatum = csv.getInt(i,"xyDatum")
  tsc.horizontalUnits = csv.getInt(i,"xyUnits")

  # tsc.setVerticalDatum(csv.getInt(i,"zDatum"))
  tsc.verticalDatum = csv.getInt(i,"zDatum")
  # tsc.setVerticalUnits(csv.getInt(i,"zUnits"))
  tsc.verticalUnits = csv.getInt(i,"zUnits")

  tsc.coordinateSystem = csv.getInt(i,"coordSys")
  tsc.coordinateID = csv.getInt(i,"coordID")

  tsc.locationTimezone = csv.getString(i,"timeZone")
  

  dss.put(tsc)
  print('\n')

print('\nDone!\n')