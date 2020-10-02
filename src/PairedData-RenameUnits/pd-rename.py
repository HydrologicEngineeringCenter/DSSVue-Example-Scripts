#replace paired data X-Units '1960 mil' with 1941
from hec.heclib.dss import HecDss
from hec.io import PairedDataContainer
import os
directory = os.path.dirname(os.path.realpath(__file__))
fileName = directory+R"\GA Degradation Bed Material.DSS"
print("filename: "+fileName)
dss = HecDss.open(fileName)
paths = dss.getPathnameList()
for p in paths:
     # using None in the next line because PartE 
     # of paths in this dss file look like dates
     pd = dss.get(p,None,None) 
     if isinstance(pd ,PairedDataContainer):
        pd.xunits = "1941"
        dss.put(pd)
dss.done()