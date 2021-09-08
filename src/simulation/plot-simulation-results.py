# ResSim, 
#https://www.hec.usace.army.mil/confluence/dssvuedocs/latest/scripting-dssvue/reading-and-writing-to-hec-dss-files
#https://www.hec.usace.army.mil/confluence/dssvuedocs/latest/scripting-dssvue/plotting-basics#id-.PlottingBasicsv2020.1-PlotClass
#file:///C:/Programs/CWMS-v3.2.2/CAVI/javaDocs/index.html
#https://www.hec.usace.army.mil/confluence/dssvuedocs/latest/scripting-dssvue/working-with-datacontainers#id-.WorkingwithDataContainersv2020.1-TimeSeriesContainerClass
from hec.script import Plot,Constants
from hec.heclib.dss import HecDss


def readFromDss(filename,Fpart, startTime, endTime) :
	dss = HecDss.open(filename, startTime, endTime)

	FOL01_LowerTierOut = dss.read("//FOLSOM-RIVER OUTLETS - LOWER TIER/FLOW-DECISION//1HOUR/" + Fpart + "/")
	FOL02_UpperTierOut = dss.read("//FOLSOM-RIVER OUTLETS - UPPER TIER/FLOW-DECISION//1HOUR/" + Fpart + "/").add(FOL01_LowerTierOut)
	FOL03_PowerPlantOut = dss.read("//FOLSOM-POWER PLANT/FLOW-DECISION//1HOUR/" + Fpart + "/").add(FOL02_UpperTierOut)
	FOL04_MainSpillway = dss.read("//FOLSOM-MAIN SPILLWAY/FLOW-DECISION//1HOUR/" + Fpart + "/").add(FOL03_PowerPlantOut)
	FOL05_EmergencySpillway = dss.read("//FOLSOM-EMERGENCY SPILLWAY/FLOW-DECISION//1HOUR/" + Fpart + "/").add(FOL04_MainSpillway)
	FOL06_DikesOverflow = dss.read("//FOLSOM-OVERFLOW/FLOW-DECISION//1HOUR/" + Fpart + "/").add(FOL05_EmergencySpillway)
	FOL07_DamLeakageOverflow = dss.read("//FOLSOM-DAM L&O/FLOW-DECISION//1HOUR/" + Fpart + "/").add(FOL06_DikesOverflow)	

	d1 = {'FOL07_DamLeakageOverflow': FOL07_DamLeakageOverflow.getData(),
	      'FOL06_DikesOverflow':FOL06_DikesOverflow.getData(), 
		  'FOL05_EmergencySpillway' : FOL05_EmergencySpillway.getData(),
		  'FOL04_MainSpillway':FOL04_MainSpillway.getData(),
		  'FOL03_PowerPlantOut': FOL03_PowerPlantOut.getData(),
		  'FOL02_UpperTierOut':FOL02_UpperTierOut.getData(), 
		  'FOL01_LowerTierOut': FOL01_LowerTierOut.getData()
		  }

	return d1

def plot_outflowCurves( outflowCurves , curveProperties) :

	thePlot = Plot.newPlot("Outflow Curves")
	layout = Plot.newPlotLayout()
	folView = layout.addViewport()

	propNames = curveProperties.get('key')
	propKeys = curveProperties.keys()
	propKeys.sort(reverse=True)
	for k in propKeys :
		row = curveProperties[k]
		curve = row[propNames.index('CurveData')]
		folView.addCurve("Y1", curve)  

	folView.setAxisName("Y1" , "Folsom")

	thePlot.configurePlotLayout(layout)

	thePlot.setPlotTitleVisible(Constants.TRUE)
	thePlot.setPlotTitleText("Outlet Releases")
	thePlot.getPlotTitle().setFontSize(18)

	thePlot.showPlot()

	propKeys = curveProperties.keys()
	print propKeys
	propNames = curveProperties.get('key')
	
	for key in propKeys :
		if key =="key":
			continue

		
		curve = thePlot.getCurve(curveProperties[key][0])
		row = curveProperties[key]
#https://www.hec.usace.army.mil/confluence/dssvuedocs/latest/scripting-dssvue/plotting-basics#id-.PlottingBasicsv2020.1-G2dLineClass
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
		curve.setFillColor(row[propNames.index('FillColor')])
		curve.setFillType("Below")
#	thePlot.stayOpen()


def go():

  forecastDSSFileName = r"C:\project\DSSVue-Example-Scripts\src\simulation\AR_Folsom_Simulation7.dss"
  startTime = "18Jan1986 2400"
  endTime = "18Mar1986 2400"
  d1 = readFromDss(forecastDSSFileName,"E504-NAT--0",startTime, endTime)

  config = {
	#	key							Curve								FillColor			 LineColor			 LineStyle		LineWeight		SymbolsVisible		SymbolType		SymbolSize				SymbolLineColor		SymbolFillColor		SymbolInterval		SymbolSkipCount		FirstSymbolOffset
	#	----------------			----------------					----------------	 -----------------	 ------------	----------		-----------------	------------	---------------------	----------------	----------------	----------------	----------------	-----------------
	    'key'						: ['CurveData',						'FillColor'        , 'LineColor'        , 'LineStyle',  'LineWeight',	'SymbolsVisible',    'SymbolType',	'SymbolSize',           'SymbolLineColor',	'SymbolFillColor',	'SymbolInterval', 'SymbolSkipCount',	'FirstSymbolOffset'],
#	----------------			----------------		----------------	------------	 -	------------	 ----------		-----------------	------------	---------------------	----------------	----------------	----------------	----------------	-----------------
		'FOL07_DamLeakageOverflow'	: [ d1['FOL07_DamLeakageOverflow'],	'lightgray'			, 'lightgray'			, 'Solid'		, 2				, Constants.FALSE	, 'none'		, Constants.UNDEFINED	, 'none'			, 'none'			, 0					, 0					, 0				] ,
		'FOL06_DikesOverflow'		: [ d1['FOL06_DikesOverflow'],	    'black'				, 'black'				, 'Solid'		, 2				, Constants.FALSE	, 'none'		, Constants.UNDEFINED	, 'none'			, 'none'			, 0					, 0					, 0				] ,
		'FOL05_EmergencySpillway'	: [ d1['FOL05_EmergencySpillway'],	'red'				, 'red'				, 'Solid'		, 2				, Constants.FALSE	, 'none'		, Constants.UNDEFINED	, 'none'			, 'none'			, 0					, 0					, 0				] ,
		'FOL04_MainSpillway'		: [ d1['FOL04_MainSpillway'],		'orange'			, 'orange'			, 'Solid'		, 2				, Constants.FALSE	, 'none'		, Constants.UNDEFINED	, 'none'			, 'none'			, 0					, 0					, 0				] ,
		'FOL03_PowerPlantOut'		: [ d1['FOL03_PowerPlantOut'],		'darkgreen'			, 'darkgreen'			, 'solid'		, 2				, Constants.FALSE	, 'none'		, Constants.UNDEFINED	, 'none'			, 'none'			, 0					, 0					, 0				] ,
		'FOL02_UpperTierOut'		: [ d1['FOL02_UpperTierOut'],		'lightblue'			, 'lightblue'			, 'Solid'		, 2				, Constants.FALSE	, 'none'		, Constants.UNDEFINED	, 'none'			, 'none'			, 0					, 0					, 0				] ,
		'FOL01_LowerTierOut'		: [ d1['FOL01_LowerTierOut'],		'lightgreen'		, 'lightgreen'		, 'Solid'		, 2				, Constants.FALSE	, 'none'		, Constants.UNDEFINED	, 'none'			, 'none'			, 0					, 0					, 0				] ,
			}


  plot_outflowCurves( d1, config )



go()
print('done')

