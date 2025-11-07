from hec.heclib.dss import HecDss
from hec.io import TimeSeriesContainer,PairedDataContainer
from hec.io import DataContainer
from hec.heclib.dss import HecDssCatalog, DSSPathname


filename = r"C:\tmp\USGSJustRes.dss"
catalog = HecDssCatalog(filename)
paths = catalog.getCondensedCatalog("")


for p in paths:
    pathname = p.getNominalPathname()
    dp = DSSPathname(pathname) 
    if dp.getCPart() == "Location Info":
    	continue
    dp.setDPart("")
    
    pathname = dp.getPathname()
    print(pathname)
    o = dss.get(pathname)
    dp.setFPart("usgs2")
    pathname = dp.getPathname()
    o.setFullName(pathname)
    print(pathname)
    if isinstance(o ,TimeSeriesContainer): 
        print("units: '" + o.units+"'")
        if o.units is None or o.units.strip() == '':
            o.units = 'ft'
            o.type = "PER-AVER"
            print("-------")
            print(o.units)
        
            dss.put(o)
