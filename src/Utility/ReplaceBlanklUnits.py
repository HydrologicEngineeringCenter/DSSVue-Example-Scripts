#replace blank/empty units with  'kcfs'
from hec.heclib.dss import HecDss
from hec.io import TimeSeriesContainer,PairedDataContainer
from hec.io import DataContainer

dss = HecDss.open("C:/temp/ensemble_test1.dss")
paths = dss.getPathnameList()
for p in paths:
    o = dss.get(p)
    if isinstance(o ,TimeSeriesContainer) or isinstance(o ,PairedDataContainer):
        print("units: '" + o.units+"'")
        if o.units is None or o.units.strip() == '':
            o.units = 'kcfs'
            dss.put(o)

dss.done()
