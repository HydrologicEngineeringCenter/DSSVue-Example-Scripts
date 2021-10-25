from hec.heclib.dss  import HecDss,DSSPathname,HecDataManager
from hec.heclib.util import HecTime,HecDouble
from hec.io import TimeSeriesContainer,TimeSeriesCollectionContainer
from hec.dataTable import	TimeSeriesDataModel
from hec.script import Constants


def getContainers(dss,tag):
	rval = TimeSeriesCollectionContainer()
	paths = dss.getCondensedCatalog()
	for cr in paths:
		p = cr.toString()
		if p.find(tag) >=0:
			pn = DSSPathname(p)
			pn.setDPart("")
			#p.setFPart()
			tsc = dss.get(pn.toString())
			
			rval.add(tsc)
	return rval

def parseValue(val):
	rval =0.0
	if isinstance(val,HecDouble):
		rval = val.value()
	elif val.toString().strip() == "":
		rval = Constants.UNDEFINED
	else:
		rval = float(val)
	return rval

def getColumnArray(m,columnIndex):
	rval = []
	numberValues = m.getRowCount()
	for i in range(0, numberValues):
		val = m.getValueAt(i,columnIndex)
		rval.append(parseValue(val))
	return rval

def getRowArray(m,rowIndex,offset):
	rval = []
	for i in range(offset, m.getColumnCount()-1):
		rval.append(parseValue(m.getValueAt(rowIndex,i)))
	return rval

def packageAsProfile(tscC, pathName):

#	rval.times = tscC.getTimes()
	m = TimeSeriesDataModel()
	m.setData([tscC],False,0)

	columns = m.getDataColumns()
	print("columns.size()"+str(columns.size()))
	print("m.getRowCount()"+str(m.getRowCount()))
	
	numberDepths = columns.size()
	numberValues = m.getRowCount()
	print ("len(numberValues): "+str(numberValues))
	
	profileDepths=[]
	for i in range(1,numberDepths):
		profileDepths.append(i*1.0)
	print ("len(profileDepths): "+str(len(profileDepths)))

	offset =3
	profileValues = []
	for i in range(offset, numberValues):
		r = getRowArray(m,i,offset)
		profileValues.append(r)
	print( profileValues	)
	
	tsc1 = tscC.get(0)
	rval = TimeSeriesContainer()
	rval.setName(pathName)
	rval.setStartTime(tsc1.startHecTime)
	rval.setProfile(profileDepths, profileValues)
	rval.setProfileDepthsUnits(tsc1.units)
	#rval.units = tsc1.units
	rval.setProfileValuesUnits(tsc1.units)
	rval.setType("Inst-Val")
	rval.profileLabel="profile - label -here"

	return rval



dss_filename = R"C:\project\DSSVue-Example-Scripts\data\forecast_data.dss"

dss = HecDss.open(dss_filename)
tscC = getContainers(dss,'T:2021.09.01-0600')
pathName="//GAPT/Version-Flow-Out//6Hour/T:2021.09.01-0600|Fcst-MRBWM-GRFT/"
profile = packageAsProfile(tscC,pathName)
dss.put(profile)

tscC = getContainers(dss,'T:2021.10.01-0600')
pathName="//GAPT/Version-Flow-Out//6Hour/T:2021.10.01-0600|Fcst-MRBWM-GRFT/"
profile = packageAsProfile(tscC,pathName)
dss.put(profile)

dss.close()


