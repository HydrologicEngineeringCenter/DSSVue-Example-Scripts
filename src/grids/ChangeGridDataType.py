# name=Change Grid Data Type
# displayinmenu=true
# displaytouser=false
# displayinselector=true

# from hec.script import MessageBox
from hec.heclib.dss import HecDss
import java
from hec.heclib.grid import GridData, GridInfo, GriddedData, GridUtilities

sourceFileName = r"C:/Temp/zMetVue/LCRA/Test/precip.dss"
destinationFileName = r"C:/Temp/zMetVue/LCRA/Test/Precip2_DSS6.dss"

inputDSS = HecDss.open(sourceFileName)	
pathnames =  inputDSS.getCatalogedPathnames()

statusArray = [0]

outputDSS = HecDss.open( destinationFileName )	

for pathname in pathnames:
	gridRecord = GridUtilities.retrieveGridFromDss(sourceFileName,pathname,statusArray)
	gridRecord.getGridInfo().setDataType(1)
	print(pathname, gridRecord.getGridInfo().getDataTypeName())
	GridUtilities.storeGridToDss(destinationFileName,pathname,gridRecord)

print('/nDone!')