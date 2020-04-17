# name=Coyote
# displayinmenu=true
# displaytouser=false
# displayinselector=true
from hec.script import *
from hec.script.Constants import TRUE, FALSE
from hec.heclib.dss import *
import java

#  grid pattern - 2 solid pixels followed by 8 blank ones
dotPat = [2., 8.]

datasets = []

#  Get the data
try :
  dssFile = HecDss.open("C:/temp/sample.dss", "01MAR2006 2400, 30MAR2006 2400")
  precip = dssFile.get("/EF RUSSIAN/COYOTE/PRECIP-INC/01MAR2006/1HOUR/TB/")
  datasets.append(precip)
  stor = dssFile.get("/EF RUSSIAN/COYOTE/STOR-RES EOP/01MAR2006/1HOUR//")
  datasets.append(stor)
  topcon = dssFile.get("/EF RUSSIAN/COYOTE/TOP CON STOR/01JAN2006/1DAY//")
  datasets.append(topcon)
  inflow = dssFile.get("/EF RUSSIAN/COYOTE/FLOW-RES IN/01MAR2006/1HOUR/SMOOTH/")
  datasets.append(inflow)
  outflow = dssFile.get("/EF RUSSIAN/COYOTE/FLOW-RES OUT/01MAR2006/1HOUR//")
  datasets.append(outflow)
  ukiah = dssFile.get("/RUSSIAN/NR UKIAH/FLOW/01MAR2006/1HOUR//")
  datasets.append(ukiah)
  hopland = dssFile.get("/RUSSIAN/NR HOPLAND/FLOW/01MAR2006/1HOUR//")
  datasets.append(hopland)
except java.lang.Exception, e :
    MessageBox.showError(e.getMessage(), "Error reading data")

#  Create the view ports
plot = Plot.newPlot("Lake Mendocino")
layout = Plot.newPlotLayout()
topView = layout.addViewport(10.)
middleView = layout.addViewport(60.)
bottomView = layout.addViewport(30.)

#  Add the data
topView.addCurve("Y1", precip)
middleView.addCurve("Y2", stor)
middleView.addCurve("Y2", topcon)
bottomView.addCurve("Y1", inflow)
bottomView.addCurve("Y1", outflow)
bottomView.addCurve("Y1", ukiah)
bottomView.addCurve("Y1", hopland)
plot.configurePlotLayout(layout)

#  For headless operation (batch mode), draw the plot off the screen
plot.setLocation(-10000, -10000)
plot.setSize(1000, 800)

####### Important – showPlot() creates the plot objects ######
# (You cannot set or change things that do not exist yet)
plot.showPlot()

#  Make the legend labels look nice
for dataset in datasets:
	label = plot.getLegendLabel(dataset)
	label.setFontSize(16)
	label.setFont("Arial Black,Plain,14")
	label.setForeground("black")

label = plot.getLegendLabel(precip)
label.setText( "Basin Precipitation")
label = plot.getLegendLabel(stor)
label.setText("Reservoir Storage")
label = plot.getLegendLabel(topcon)
label.setText("Top of Connservaion")
label = plot.getLegendLabel(inflow)
label.setText("Inflow")
label = plot.getLegendLabel(outflow)
label.setText("Outflow")
label = plot.getLegendLabel(ukiah)
label.setText("Russian near Ukiah")
label = plot.getLegendLabel(hopland)
label.setText("Russian near Hopland")

#  Set the plot title
plot.setPlotTitleText("Lake Mendocino (Coyote Valley Dam) - Russian River Basin")
tit = plot.getPlotTitle()
tit.setFont("Arial Black")
tit.setFontSize(18)
plot.setPlotTitleVisible(TRUE)

#  Make the viewports right next to each other
panel = plot.getPlotpanel()
panel.setHorizontalViewportSpacing(0)

#  Set the Y axis labels
view0 = plot.getViewport(0)
yaxis = view0.getAxis("Y1")
yaxis.setReversed(FALSE)
yaxis.setLabel("PPT")
view1 = plot.getViewport(1)
yaxis1 = view1.getAxis("Y2")
yaxis1.setLabel("Storage (ACFT)")
yaxis1.setScaleLimits(0., 140000.)
yaxis1.setViewLimits(0., 140000.)

#  Mark the gross pool level
marker = AxisMarker()
marker.axis = "Y"
marker.value = "118000"
marker.labelText = "Gross Pool"
marker.lineColor = "Blue"
marker.labelPosition = "center"
view1.addAxisMarker(marker)

#  Set the curve colors and fill
precipCurve = plot.getCurve(precip)
precipCurve.setFillColor("blue")
precipCurve.setFillType("Above")
precipCurve.setLineColor("blue")

conCurve = plot.getCurve(topcon)
conCurve.setFillColor("lightGray")
conCurve.setFillType("Below")
conCurve.setLineColor("lightGray")

storCurve = plot.getCurve(stor)
storCurve.setLineColor("blue")
storCurve.setLineWidth(1.)

outCurve = plot.getCurve(outflow)
outCurve.setLineColor("darkgreen")
outCurve.setLineWidth(1.)

inCurve = plot.getCurve(inflow)
inCurve.setLineColor("red")
inCurve.setLineWidth(1.)

ukiahCurve = plot.getCurve(ukiah)
ukiahCurve.setLineColor("magenta")
ukiahCurve.setLineWidth(1.)

hoplandCurve = plot.getCurve(hopland)
hoplandCurve.setLineColor("blue")
hoplandCurve.setLineWidth(1.)

#  Set grid style
view0 = plot.getViewport(0)
prop = view0.getProperties()
prop.setMajorXGridStyle(dotPat)
prop.setMajorYGridStyle(dotPat)
view1 = plot.getViewport(1)
prop = view1.getProperties()
prop.setMajorXGridStyle(dotPat)
prop.setMajorYGridStyle(dotPat)
view2 = plot.getViewport(2)
prop = view2.getProperties()
prop.setMajorXGridStyle(dotPat)
prop.setMajorYGridStyle(dotPat)

#  Now that it is complete, save to a png and close it
plot.saveToPng("C:/temp/Coyote.png")
plot.close()
