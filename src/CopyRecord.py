from hec.heclib.dss import HecDss

sourceFile      = R"C:\project\DSSVue-Example-Scripts\data\examples-all-data-types.dss"
destinationFile = R"C:\tmp\copied_records.dss"

pathnames = [
    "/time-series-group-1/LAKE MENDOCINO/FLOW-IN//1HOUR/C:000005|T:20211221-1200|V:20211221-095000|SHORT RANGE HOURLY ENSEMBLE CSV FILE DOWNLOAD/", # time series
    "/grid/EAU GALLA RIVER/SNOW MELT/02FEB2020:0600/03FEB2020:0600/SHG-SNODAS/", # grid
]
source      = HecDss.open(sourceFile)
destination = HecDss.open(destinationFile)

for pathname in pathnames:
    container = source.get(pathname)          
    container.fileName = None  
    destination.put(container) 
    print("Copied %s", pathname)

source.close()
destination.close()
print("Done.  Wrote to " + destinationFile)
