from hec.io import ArrayContainer
from hec.heclib.dss import HecDssArray
from jarray import array

ac = ArrayContainer()
ac.setFloatArray([1.0, 2.0, 3.14])

dss = HecDssArray("c:/temp/myFile.dss")
dss.setPathname("//script/data///test/")
dss.write(ac)
