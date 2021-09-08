from hec.heclib.dss import HecDss
from hec.script import Plot

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

	# add incremental
	upper = upper.add(lower)
	power = power.add(upper)
	mainSpill = mainSpill.add(power)
	eSpill = eSpill.add(mainSpill)
	dikes = dikes.add(eSpill)
	leakage = leakage.add(dikes)
	#package up data to return from function
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


# organize and manipulate data

# customize plot with final data


def makeOutflowPlot():
	filename = "C:\Temp\AR_Folsom_Simulation7.dss"
	t1 = "18Jan1986 2400"
	t2 = "18Mar1986 2400"
	dssData = readDssFile(filename,t1,t2)
	
	
	p = Plot.newPlot("Folsom simulation")
	p.addData(dssData['upper'])
	p.addData(dssData['lower'])
	
	p.showPlot()
	print("Hi")
	print(dssData)
	print(dssData['upper'])

makeOutflowPlot()