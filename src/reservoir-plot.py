# name=0 ResSum Plots - C Drive
# displayinmenu=true
# displaytouser=true
# displayinselector=true
from hec.heclib.util import HecTime					# always needed - time window options
from hec.script import Plot, Tabulate				# always needed - plots and tables
from hec.script.Constants import TRUE, FALSE		# always needed - true/false
import DBAPI, hec, sys								# always needed
import datetime


OutputFolder = r"C:/My Documents/Reservoir Operations/Old Reports/"
now = datetime.datetime.now()
db = DBAPI.open()
db.setTimeZone("US/Central")


def plotReservoir(title, elevationID, inflowID, outflowID, fileNameSuffix):
    """ creates a Reservoir plot with Elevation, Inflow and Outflow """
    elev = db.get(elevationID)
    inflow = db.get(inflowID)
    flow = db.get(outflowID)

    plotF = Plot.newPlot()
    plotLayout = Plot.newPlotLayout()
    vpTop = plotLayout.addViewport(30)
    vpTop.addCurve("Y1", elev)
    vpBottom = plotLayout.addViewport(70)
    vpBottom.addCurve("Y1", inflow)
    vpBottom.addCurve("Y1", flow)
    plotF.configurePlotLayout(plotLayout)
    plotF.setUseLineStylesOff()
    plotF.showPlot()
    plotF.setLegendLabelText(elev, "Reservoir Pool Elevation - Forecast")
    plotF.setLegendLabelText(inflow, "Reservoir Inflow - Forecast")
    plotF.setLegendLabelText(flow, "Reservoir Outflow - Forecast")
    plotF.setPlotTitleText(title+"    Generated: " + now.strftime("%Y%m%d %H:%M:%S "))
    tit = plotF.getPlotTitle()
    tit.setFont("Arial")
    tit.setFontSize(16)
    plotF.setPlotTitleVisible(TRUE)
    plotF.setLocation(50,50)
    plotF.setSize(1000,700)
    Data32Curve = plotF.getCurve(elev)
    Data32Curve.setLineColor("lightblue")
    Data32Curve.setLineWidth(2.)
    Data32Curve.setLineStyle("dot")
    Data34Curve = plotF.getCurve(inflow)
    Data34Curve.setLineColor("red")
    Data34Curve.setLineWidth(2.)
    Data34Curve.setLineStyle("dot")
    Data36Curve = plotF.getCurve(flow)
    Data36Curve.setLineColor("lightblue")
    Data36Curve.setLineWidth(2.)
    Data36Curve.setLineStyle("dot")
    # 
    fileName = OutputFolder+"ResSumPlot-"+fileNameSuffix+"png"
    plotF.saveToPng(fileName)






startTime = HecTime()
endTime   = HecTime()
HecTime.getTimeWindow("t 0600 t+5d", startTime, endTime) # use a fixed time window
db.setTimeWindow(startTime.dateAndTime(104), endTime.dateAndTime(104))
extraTitle=startTime.dateAndTime(104)+" "+endTime.dateAndTime(104)

plotReservoir('Kinzua Dam and Allegheny Reservoir', # title
              'Kinzua-Lake.Elev.Inst.1Hour.0.RESOPS',  
              'Kinzua-Lake.Flow-Inflow-Comp.Inst.1Hour.0.RESOPS',
              'Kinzua-Outflow.Flow.Inst.1Hour.0.RESOPS',
              'A') # filename suffix



plotReservoir('Mahoning Creek Lake', # title
              'Mahoning-Lake.Elev.Inst.1Hour.0.RESOPS',  
              'Mahoning-Lake.Flow-Inflow-Comp.Inst.1Hour.0.RESOPS',
              'Mahoning-Outflow.Flow.Inst.1Hour.0.RESOPS',
              'F') # filename suffix


db.done()

 
