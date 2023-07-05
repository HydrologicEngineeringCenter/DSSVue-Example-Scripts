from hec.script      import AxisMarker
from hec.script      import Plot
from hec.heclib.dss  import HecDss
from hec.heclib.util import HecTime
from hec.hecmath     import TimeSeriesMath
import os

def main() :
	#
	# setup
	#
	dssFilename     = "C:/Class/DSS/Customizing HEC-DSSVue/CustomizingDSSVueWorkshopData.dss"
	startTime       = "01JAN2009 0000"
	endTime         = "31DEC2009 2400"
	precipPathname  = "//PENS/PRECIP//1HOUR/OBS/"
	elevPathname    = "//PENS/ELEV//1HOUR/OBS/"
	storPathname    = "//PENS/STOR-RES EOP//1HOUR/OBS/"
	inflowPathname  = "//PENS/FLOW-RES IN//1HOUR/OBS/"
	outflowPathname = "//PENS/FLOW-RES OUT//1HOUR/OBS/"
	#
	# open the DSS file and read the data
	#
	dssFile = HecDss.open(dssFilename)
	dssFile.setTimeWindow(startTime, endTime)
	precipData  = dssFile.read(precipPathname).successiveDifferences().getData()
	elevData    = dssFile.get(elevPathname)
	storData    = dssFile.get(storPathname)
	inflowData  = dssFile.get(inflowPathname)
	outflowData = dssFile.get(outflowPathname)
	dssFile.done()
	#
	# generate a plot layout
	#
	plotLayout = Plot.newPlotLayout()
	vpTop = plotLayout.addViewport(10)
	vpTop.addCurve("Y1", precipData)
	vpMiddle = plotLayout.addViewport(45)
	vpMiddle.addCurve("Y1", elevData)
	vpMiddle.addCurve("Y2", storData)
	vpBottom = plotLayout.addViewport(45)
	vpBottom.addCurve("Y1", outflowData)
	vpBottom.addCurve("Y1", inflowData)
	#
	# Generate the plot from the plot layout
	#
	plot = Plot.newPlot("ReservoirPlot")
	plot.configurePlotLayout(plotLayout)
	plot.showPlot()
	plot.getPlotpanel().setHorizontalViewportSpacing(0)
	#
	# setup the plot title
	#
	plot.setPlotTitleText("Grand Lake o' the Cherokees")
	plot.setPlotTitleVisible(True)
	title = plot.getPlotTitle()
  # Setting Font and Size in the Title
	title.setFont("Tahoma,Bold ITALIC,16")
	title.setFont("Times New Roman, italic,16")
	title.setBackgroundVisible(False)
	#
	# customize the legend text
	#
	plot.setLegendLabelText(precipData,  "Precip")
	plot.setLegendLabelText(elevData,    "Elevation")
	plot.setLegendLabelText(storData,    "Storage")
	plot.setLegendLabelText(inflowData,  "Inflow")
	plot.setLegendLabelText(outflowData, "Releases")
	#
	# reverse the precip axis
	#
	precipViewport = plot.getViewport(0)
	precipAxis = precipViewport.getAxis("Y1")
	precipAxis.setReversed(False)
	#
	# normalize the scale of the storage axis
	#
	storViewport = plot.getViewport(1)
	storViewport.scaleAxisFromOpposite("Y2")
	#
	# customize the curve properties
	#
	precipCurve = plot.getCurve(precipData)
	precipCurve.setLineColor("Darkblue")
	precipCurve.setLineWidth(1)
	precipCurve.setLineStyle("Solid")
	precipCurve.setFillType("Above")
	precipCurve.setFillColor("Darkblue")
	precipCurve.setFillPattern("Solid")
	
	elevCurve = plot.getCurve(elevData)
	elevCurve.setLineVisible(True)
	elevCurve.setLineColor("Red")
	elevCurve.setLineWidth(1)
	elevCurve.setLineStyle("Solid")
	elevCurve.setSymbolsVisible(True)
	elevCurve.setSymbolType("circle")
	elevCurve.setSymbolSize(7)
	elevCurve.setSymbolLineColor("Red")
	elevCurve.setSymbolFillColor("Red")
	elevCurve.setSymbolsAutoInterval(False)
	elevCurve.setFirstSymbolOffset(0) # comment this out if using AutoInterval
	elevCurve.setSymbolSkipCount(23)  # comment this out if using AutoInterval
	elevCurve.setFillType("Below")
	elevCurve.setFillColor("Red")
	elevCurve.setFillPattern("Diagonal Cross")
	
	storCurve = plot.getCurve(storData)
	storCurve.setLineVisible(True)
	storCurve.setLineColor("Blue")
	storCurve.setLineWidth(1)
	storCurve.setLineStyle("Solid")
	storCurve.setSymbolsVisible(True)
	storCurve.setSymbolType("Open Square")
	storCurve.setSymbolSize(7)
	storCurve.setSymbolLineColor("Blue")
	storCurve.setSymbolFillColor(None)
	storCurve.setSymbolsAutoInterval(False)
	storCurve.setFirstSymbolOffset(12) # comment this out if using AutoInterval
	storCurve.setSymbolSkipCount(23)   # comment this out if using AutoInterval
	storCurve.setFillType(None)
	storCurve.setFillColor(None)
	storCurve.setFillPattern(None)
	
	outflowCurve = plot.getCurve(outflowData)
	outflowCurve.setLineVisible(True)
	outflowCurve.setLineColor("DarkRed")
	outflowCurve.setLineWidth(2)
	outflowCurve.setLineStyle("Solid")
	outflowCurve.setSymbolsVisible(False)
	outflowCurve.setSymbolType("Triangle2")
	outflowCurve.setSymbolSize(7)
	outflowCurve.setSymbolLineColor("DarkRed")
	outflowCurve.setSymbolFillColor("DarkRed")
	outflowCurve.setSymbolsAutoInterval(False)
	outflowCurve.setFirstSymbolOffset(12) # comment this out if using AutoInterval
	outflowCurve.setSymbolSkipCount(23)   # comment this out if using AutoInterval
	outflowCurve.setFillType("Below")
	outflowCurve.setFillColor("DarkPink")
	outflowCurve.setFillPattern("Solid")
	
	inflowCurve = plot.getCurve(inflowData)
	inflowCurve.setLineVisible(True)
	inflowCurve.setLineColor("DarkGreen")
	inflowCurve.setLineWidth(1)
	inflowCurve.setLineStyle("Solid")
	inflowCurve.setSymbolsVisible(False)
	inflowCurve.setSymbolType("Triangle")
	inflowCurve.setSymbolSize(7)
	inflowCurve.setSymbolLineColor("Darkgreen")
	inflowCurve.setSymbolFillColor("Darkgreen")
	inflowCurve.setSymbolsAutoInterval(False)
	inflowCurve.setFirstSymbolOffset(0) # comment this out if using AutoInterval
	inflowCurve.setSymbolSkipCount(23)  # comment this out if using AutoInterval
	inflowCurve.setFillType(None)
	inflowCurve.setFillColor(None)
	inflowCurve.setFillPattern(None)
	#
	# add an axis marker for the maximum elevation
	#
	elevMath = TimeSeriesMath(elevData)
	maxElev = elevMath.max()
	maxElevTime = HecTime()
	maxElevTime.set(elevMath.maxDate())
	maxElevMarker = AxisMarker()
	maxElevMarker.axis = "Y1"
	maxElevMarker.value = "%f" % maxElev
	maxElevMarker.lineColor = elevCurve.getLineColorString()
	maxElevMarker.lineWidth = 1
	maxElevMarker.lineStyle = "dash"
	maxElevMarker.fillStyle = None
	maxElevMarker.fillColor = maxElevMarker.lineColor
	maxElevMarker.fillPattern = None
	maxElevMarker.labelText = "Max Elev = %.2f at %s" % (maxElev, maxElevTime.dateAndTime(104))
	maxElevMarker.labelColor = maxElevMarker.lineColor
  # Setting Font and Size in the AxisMarker
	maxElevMarker.labelFont = "Times New Roman,bold italic,14"
	maxElevMarker.labelPosition = "Above"
	maxElevMarker.labelAlignment = "Left"
	plot.getViewport(1).addAxisMarker(maxElevMarker)
	#
	# set the viewport color
	#
	for viewport in plot.getViewports() :
		viewport.setBackground("248,248,248")
		viewport.setBackgroundVisible(True)
	#
	# resize the plot and save to an image file
	#
	workshopDir = os.path.split(dssFilename)[0]
	plotFilename = os.path.join(workshopDir, "ReservoirPlot.png")
	oldSize = plot.getSize()
	plot.setSize(1200, 600)
	plot.saveToPng(plotFilename)
	#
	# restore the plot size and modify the title for display
	#
	plot.setSize(oldSize.width, oldSize.height)
	title.setBorderVisible(False)
	title.setBackgroundVisible(False)

if __name__ == "__main__" :
	main()
