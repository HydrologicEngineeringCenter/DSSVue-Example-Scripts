from hec.heclib.dss import HecDss, DSSPathname
from hec.script import Plot
from hec.dssgui import ListSelection

def readDssFile(filename,startTime, endTime):
	dss = HecDss.open(filename, startTime, endTime)	
	
	pathEnd = "/FLOW-DECISION//1Hour/E504-NAT--0/"

	lower = dss.read("//FOLSOM-RIVER OUTLETS - LOWER TIER"+pathEnd)
	upper = dss.read("//FOLSOM-RIVER OUTLETS - UPPER TIER"+pathEnd)
	power = dss.read("//FOLSOM-POWER PLANT"+pathEnd)
	mainSpill = dss.read("//FOLSOM-MAIN SPILLWAY"+pathEnd)
	eSpill = dss.read("//FOLSOM-EMERGENCY SPILLWAY"+pathEnd)
	dikes = dss.read("//FOLSOM-OVERFLOW"+pathEnd)
	leakage = dss.read("//FOLSOM-DAM L&O"+pathEnd)

	# make data incremental (stackable)
	upper = upper.add(lower)
	power = power.add(upper)
	mainSpill = mainSpill.add(power)
	eSpill = eSpill.add(mainSpill)
	dikes = dikes.add(eSpill)
	leakage = leakage.add(dikes)
	#package up data, as dictionary, to return from function
	allData ={'lower':lower.getData(),
			  'upper':upper.getData(),
			  'power': power.getData(),
			  'mainSpill': mainSpill.getData(),
			  'eSpill': eSpill.getData(),
			  'dikes': dikes.getData(),
			  'leakage': leakage.getData()
			} 
	
	return allData
	#print(leakage.getData().values)


# customize plot curves with final data
def setCurveProperties(p,tsc,color,style):
	curve= p.getCurve(tsc)
	curve.setLineColor(color)
	curve.setFillColor(color)
	curve.setLineStyle(style)
	curve.setFillType('Below')

def makeOutflowPlot():
	filename = "C:\Temp\AR_Folsom_Simulation7.dss"
	t1 = "18Jan1986 2400"
	t2 = "18Mar1986 2400"
	dssData = readDssFile(filename,t1,t2)
	
	p = Plot.newPlot("Outflow Curves")

	p.addData(dssData['leakage'])
	p.addData(dssData['dikes'])
	p.addData(dssData['eSpill'])
	p.addData(dssData['mainSpill'])
	p.addData(dssData['power'])
	p.addData(dssData['upper'])
	p.addData(dssData['lower'])

	p.showPlot()

	setCurveProperties(p,dssData['upper'],'lightgreen','Solid')
	setCurveProperties(p,dssData['lower'],'lightblue','Solid')
	setCurveProperties(p,dssData['power'],'darkgreen','Solid')
	setCurveProperties(p,dssData['mainSpill'],'orange','Solid')
	setCurveProperties(p,dssData['eSpill'],	'red','Solid')
	setCurveProperties(p,dssData['dikes'], 'black','Solid')
	setCurveProperties(p,dssData['leakage'],'lightgray','Solid')

	if( not ListSelection.isInteractive()):
		p.stayOpen()


makeOutflowPlot()