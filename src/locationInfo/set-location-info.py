from hec.script import Plot
from hec.heclib.dss import HecDss, DSSPathname
import csv
 
class csvfile:

  def __init__(self, filename):
    raw=list(csv.reader(open(filename)))
    self.column_names =raw[0] 
    self.data = raw[1:]

  def getString(self,rowIndex,column_name):
    colIndex = self.column_names.index(column_name)
    print(colIndex)
    return self.data[rowIndex][colIndex]

  def getFloat(self,rowIndex,column_name):
    s = self.getString(rowIndex,column_name)
    return float(s)

  def size(self):
    return len(self.data)

# begin main program
# note: location info can be created when saving a specific timeseriescontainer
# however, location info can't be modified as part of a timeseries container
# because that location info is potentially  shared with other containers

csv = csvfile(r"C:/tmp/location.csv")
fn =r"c:/tmp/lat-long-test.dss"
dss = HecDss.open(fn)

for i in range(0,csv.size()):
  path = csv.getString(i,"pathname")
  dssPath = DSSPathname(path)
  dssPath.setDPart("") # remove dates from path
  tsc=dss.get(dssPath.pathname())
  print(csv.getFloat(i,"x"))
  tsc.setLatLong(csv.getFloat(i,"x"),csv.getFloat(i,"y"))
  dss.put(tsc)

