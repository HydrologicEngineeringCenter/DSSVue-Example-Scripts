from hec.heclib.dss import HecDss
from hec.io import TimeSeriesContainer,PairedDataContainer
from hec.io import DataContainer

dss = HecDss.open("C:/temp/a.dss")
paths = dss.getPathnameList()
for p in paths:
    o = dss.get(p)
    if isinstance(o ,TimeSeriesContainer): 
        print("units: '" + o.units+"'")
        if o.units is None or o.units.strip() == '':
            o.units = 'kcfs'
            dss.put(o)
    if isinstance(o ,PairedDataContainer): 
        print("units: '" + o.yunits+"'")
        if o.units is None or o.xunits.strip() == '':
            o.xunits = 'x'
            o.yunits = 'kcfs'
            #o.xtype =
            #o.ytype=
            dss.put(o)

dss.done()
