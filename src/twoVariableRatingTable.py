from hec.io import TimeSeriesContainer
from hec.hecmath import TimeSeriesMath
from hec.hecmath import PairedDataMath

from hec.heclib.dss import HecDss

def twoVariableInterpolate(dss, tablePath, flowPath, elevationPath):
	
	pdMath = PairedDataMath()
	pdMath.setData(dss.get(tablePath))

	mathFlow = TimeSeriesMath()
	mathFlow.setData(dss.get(flowPath))

	mathElev = TimeSeriesMath()
	mathElev.setData(dss.get(elevationPath))
	outMath = pdMath.twoVariableRatingTableInterpolation(mathFlow, mathElev)
	rval = TimeSeriesContainer()
	outMath.getData(rval)
	rval.modified = True	
	return rval


filename = r"C:\tmp\TwoVariableRating.dss"
dss = HecDss.open(filename)
table = "/Missouri Rv at Williston-WSN/Rating Curve-IV_3VAR/Flow-Stage////"
flow = "//GARR-INFLOW/FLOW//1Day/C:000001|WITHOUT PR:50 YR:RESSIM-MM2018MC/"
elev = "//LAKE SAKAKAWEA-POOL/ELEV//1Day/C:000001|WITHOUT PR:50 YR:RESSIM-MM2018MC/"
output = "//GARR-INFLOW/Stage//1Day/test/"
tsc = twoVariableInterpolate(dss,table, flow, elev)

tsc.printToConsole(30)  # print first 30 values to the console

tsc.setFullName(output)
dss.put(tsc)
