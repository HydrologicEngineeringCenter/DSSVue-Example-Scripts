from hec.heclib.dss import HecDss
from hec.model import PairedValuesExt

pname = '/paired-data/DEER CREEK/STAGE-FLOW///USGS/'
dss_file = r'data\examples-all-data-types.dss'

fid = HecDss.Open(dss_file)
pdc = fid.get(pname)

table = PairedValuesExt()
table.setData(pdc)

print(table.interpolate(5.22))

fid.close()

