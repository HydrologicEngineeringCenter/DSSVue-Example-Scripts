from hec.script import Plot,Constants
from hec.io import TimeSeriesContainer
from hec.heclib.util import HecTime
from hec.heclib.dss import HecDss


def readFromDss(filename,Fpart, startTime, endTime) :
	dss = HecDss.open(filename, startTime, endTime)

	FOL01_LowerTierOut = dss.read("//FOLSOM-RIVER OUTLETS - LOWER TIER/FLOW-DECISION//1HOUR/" + Fpart + "/")
	FOL02_UpperTierOut = dss.read("//FOLSOM-RIVER OUTLETS - UPPER TIER/FLOW-DECISION//1HOUR/" + Fpart + "/").add(FOL01_LowerTierOut)
	FOL03_PowerPlantOut = dss.read("//FOLSOM-POWER PLANT/FLOW-DECISION//1HOUR/" + Fpart + "/").add(FOL02_UpperTierOut)
	FOL04_MainSpillway = dss.read("//FOLSOM-MAIN SPILLWAY/FLOW-DECISION//1HOUR/" + Fpart + "/").add(FOL03_PowerPlantOut)
	FOL05_EmergentySpillway = dss.read("//FOLSOM-EMERGENCY SPILLWAY/FLOW-DECISION//1HOUR/" + Fpart + "/").add(FOL04_MainSpillway)
	FOL06_DikesOverflow = dss.read("//FOLSOM-OVERFLOW/FLOW-DECISION//1HOUR/" + Fpart + "/").add(FOL05_EmergentySpillway)
	FOL07_DamLeakageOverflow = dss.read("//FOLSOM-DAM L&O/FLOW-DECISION//1HOUR/" + Fpart + "/").add(FOL06_DikesOverflow)	

	d1 = {'FOL07_DamLeakageOverflow': FOL07_DamLeakageOverflow.getData(),
	      'FOL06_DikesOverflow':FOL06_DikesOverflow, 
		  'FOL05_EmergentySpillway' : FOL04_MainSpillway,
						'FOL03_PowerPlantOut': FOL03_PowerPlantOut,
						'FOL02_UpperTierOut':FOL02_UpperTierOut, 
						 'FOL01_LowerTierOut': FOL01_LowerTierOut
		  }
	outflowCurves = [	FOL07_DamLeakageOverflow.getData(), FOL06_DikesOverflow.getData(), 
						FOL05_EmergentySpillway.getData(), FOL04_MainSpillway.getData(),
						FOL03_PowerPlantOut.getData(),
						FOL02_UpperTierOut.getData(),  FOL01_LowerTierOut.getData()		]


	return outflowCurves

def plot_outflowCurves( outflowCurves , curveProperties) :

	thePlot = Plot.newPlot("Outflow Curves")
	layout = Plot.newPlotLayout()

	folView = layout.addViewport()


	folViewDC = []
	for i in range(len(outflowCurves)) :
		dc =  outflowCurves[i] #.getData()
		folViewDC.append(dc)

  	
	for x in range(len(outflowCurves)) :
		folView.addCurve("Y1", outflowCurves[x])

	folView.setAxisName("Y1" , "Folsom")

	thePlot.configurePlotLayout(layout)

	thePlot.setPlotTitleVisible(Constants.TRUE)
	thePlot.setPlotTitleText("Outlet Releases")
	#thePlot.getPlotTitle().setFont("Arial Black")
	thePlot.getPlotTitle().setFontSize(18)

	thePlot.showPlot()
	#thePlot.stayOpen()
	#folV = thePlot.getViewport(0)
	#folViewY1Axis = folV.getAxis("Y1")
	#folViewY1Axis.setScaleLimits(0, 1.0e7)
	#folViewY1Axis.setLabel("Outflow (cfs)")


	propKeys = curveProperties.keys()
	print propKeys
	propKeys.sort()
	print propKeys
	propNames = curveProperties.get('key')
	
	for key in propKeys :
		if key =="key":
			continue
		
		curve = thePlot.getCurve(curveProperties[key][0])
		row = curveProperties[key]

		curve.setLineColor(row[propNames.index('LineColor')])
		curve.setLineStyle(row[propNames.index('LineStyle')])
		curve.setLineWidth(row[propNames.index('LineWeight')])
		curve.setSymbolsVisible(row[propNames.index('SymbolsVisible')])
		curve.setSymbolType(row[propNames.index('SymbolType')])
		curve.setSymbolSize(row[propNames.index('SymbolSize')])
		curve.setSymbolLineColor(row[propNames.index('SymbolLineColor')])
		curve.setSymbolFillColor(row[propNames.index('SymbolFillColor')])
		curve.setSymbolInterval(row[propNames.index('SymbolInterval')])
		curve.setSymbolSkipCount(row[propNames.index('SymbolSkipCount')])
		curve.setFirstSymbolOffset(row[propNames.index('FirstSymbolOffset')])
		curve.setFillPattern("Solid")
		curve.setFillType("Below")
	thePlot.stayOpen()


def go():

  forecastDSSFileName = r"C:\project\DSSVue-Example-Scripts\src\simulation\AR_Folsom_Simulation7.dss"
  startTime = "18Jan1986 2400"
  endTime = "18Mar1986 2400"

  outflowCurves = readFromDss(forecastDSSFileName,"E504-NAT--0",startTime, endTime)

  config = {
	#	key							Curve					LineColor			LineStyle		LineWeight		SymbolsVisible		SymbolType		SymbolSize				SymbolLineColor		SymbolFillColor		SymbolInterval		SymbolSkipCount		FirstSymbolOffset
	#	----------------			----------------		----------------	------------	----------		-----------------	------------	---------------------	----------------	----------------	----------------	----------------	-----------------
	    'key'						: ['Curve',				'LineColor'        , 'LineStyle',  'LineWeight',	'SymbolsVisible',    'SymbolType',	'SymbolSize',           'SymbolLineColor',	'SymbolFillColor',	'SymbolInterval', 'SymbolSkipCount',	'FirstSymbolOffset'],
#	----------------			----------------		----------------	------------	----------		-----------------	------------	---------------------	----------------	----------------	----------------	----------------	-----------------
		'FOL07_DamLeakageOverflow'	: [ outflowCurves[0],	'lightgray'			, 'Solid'		, 2				, Constants.FALSE	, 'none'		, Constants.UNDEFINED	, 'none'			, 'none'			, 0					, 0					, 0				] ,
		'FOL06_DikesOverflow'		: [ outflowCurves[1],	'black'				, 'Solid'		, 2				, Constants.FALSE	, 'none'		, Constants.UNDEFINED	, 'none'			, 'none'			, 0					, 0					, 0				] ,
		'FOL05_EmergentySpillway'	: [ outflowCurves[2],	'red'				, 'Solid'		, 2				, Constants.FALSE	, 'none'		, Constants.UNDEFINED	, 'none'			, 'none'			, 0					, 0					, 0				] ,
		'FOL04_MainSpillway'		: [ outflowCurves[3],	'orange'			, 'Solid'		, 2				, Constants.FALSE	, 'none'		, Constants.UNDEFINED	, 'none'			, 'none'			, 0					, 0					, 0				] ,
		'FOL03_PowerPlantOut'		: [ outflowCurves[4],	'darkgreen'			, 'solid'		, 2				, Constants.FALSE	, 'none'		, Constants.UNDEFINED	, 'none'			, 'none'			, 0					, 0					, 0				] ,
		'FOL02_UpperTierOut'		: [ outflowCurves[5],	'lightblue'			, 'Solid'		, 2				, Constants.FALSE	, 'none'		, Constants.UNDEFINED	, 'none'			, 'none'			, 0					, 0					, 0				] ,
		'FOL01_LowerTierOut'		: [ outflowCurves[6],	'lightgreen'		, 'Solid'		, 2				, Constants.FALSE	, 'none'		, Constants.UNDEFINED	, 'none'			, 'none'			, 0					, 0					, 0				] ,
			}


  plot_outflowCurves( outflowCurves, config )



go()
print('done')

