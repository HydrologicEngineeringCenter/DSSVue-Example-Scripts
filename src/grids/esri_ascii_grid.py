from hec.heclib.grid import Dss2AscGrid
from hec.heclib.grid import Asc2DssGrid

# write a DSS Gridded record to ESRI ASCII( Grid 
#https://desktop.arcgis.com/en/arcmap/latest/manage-data/raster-and-images/esri-ascii-raster-format.htm

TXT_FILE = r"C:\project\DSSVue-Example-Scripts\src\grids\grid.txt"
OUTPUT_DSS = r"C:\project\DSSVue-Example-Scripts\src\grids\out.dss"
INPUT_DSS = r"C:\project\DSSVue-Example-Scripts\data\TC_0657.dss"
DSS_PATH = "/SHG/NECHES/PRECIP_TX_0657/04JUL2000:0000/04JUL2000:0100/PROJECTED_WGS84_ALBERS/"
args = ["OUTPUT="+TXT_FILE, "DSSFILE="+INPUT_DSS,"PATHNAME="+DSS_PATH]
d2a = Dss2AscGrid(args)
d2a.dump();

##  Read ESRI ASCII Grid and save to DSS
# *
# *  Arguments: input: name of ASCII file data from an Arc/Info grid
# *             dssfile:  Name of the DSS file to which the gridded data
# *                       record will be written
# *             pathname: The DSS path name for the gridded data record
# *             gridType: The grid type (HRAP, SHG, etc.)
# *             dunits:   DSS data units
# *             dtype:    DSS data type
args = ["input="+TXT_FILE, "dssfile="+OUTPUT_DSS, "pathname="+DSS_PATH,
      "gridtype=SHG", "dunits=inches",  "dtype=PER-AVER" ]
 
 
a2d = Asc2DssGrid(args)
a2d.load()
