from hec.heclib.dss import HecDss
from hec.heclib.grid import GridData, GridInfo, GriddedData, GridUtilities

statusArray = [0]
dssFilename = "C:\project\DSSVue-Example-Scripts\data\examples-all-data-types.dss"
pathname ="/grid/EAU GALLA RIVER/SNOW MELT/02FEB2020:0600/03FEB2020:0600/SHG-SNODAS/"

gridRecord = GridUtilities.retrieveGridFromDss(dssFilename,pathname,statusArray)

pathname ="/grid/EAU GALLA RIVER/SNOW MELT/02FEB2020:0600/03FEB2020:0600/SHG-SNODAS-update/"
info = gridRecord.getGridInfo()
info.setGridTimes("02jan2000 12:00","02jan2000 13:00")
GridUtilities.storeGridToDss(dssFilename,pathname,gridRecord)



