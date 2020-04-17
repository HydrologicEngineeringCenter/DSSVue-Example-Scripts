# name=Folsom
# displayinmenu=true
# displaytouser=true
# displayinselector=true
from hec.script import *
from hec.script.Constants import TRUE, FALSE
from hec.heclib.dss import *
import java

#  Open the file and get the data
try:  
  dssFile = HecDss.open("C:/temp/sample.dss", "10MAR2006 2400, 09APR2006 2400")
  precip = dssFile.get("/AMERICAN/FOLSOM/PRECIP-BASIN/01JAN2006/1DAY/OBS/")
  stor = dssFile.get("/AMERICAN/FOLSOM/ STOR-RES EOP/01JAN2006/1DAY/OBS/")
  topcon = dssFile.get("/AMERICAN/FOLSOM/TOP CON STOR/01JAN2006/1DAY/OBS/")
  sagca = dssFile.get("/AMERICAN/FOLSOM-SAGCA/TOP CON STOR/01JAN2006/1DAY/OBS/")
  inflow = dssFile.get("/AMERICAN/FOLSOM/FLOW-RES IN/01JAN2006/1DAY/OBS/")
  outflow = dssFile.get("/AMERICAN/FOLSOM/FLOW-RES OUT/01JAN2006/1DAY/OBS/")
except java.lang.Exception, e :
  #  Take care of any missing data or errors
   MessageBox.showError(e.getMessage(), "Error reading data")

#  Initialize the plot and set viewport size in precent
plot = Plot.newPlot("Folsom - American River Basin")
layout = Plot.newPlotLayout()
topView = layout.addViewport(10.)
middleView = layout.addViewport(60.)
bottomView = layout.addViewport(30.)

#  Add Data in specific viewports
topView.addCurve("Y1", precip)
middleView.addCurve("Y2", stor)
middleView.addCurve("Y2", topcon)
middleView.addCurve("Y2", sagca)
bottomView.addCurve("Y1", inflow)
bottomView.addCurve("Y1", outflow)

panel = plot.getPlotpanel()
prop = panel.getProperties()
prop.setViewportSpaceSize(0)

#  Break our first rule - actually this creates the plot to change
plot.configurePlotLayout(layout)

panel = plot.getPlotpanel()
prop = panel.getProperties()
prop.setViewportSpaceSize(0)

#  Invert the precip and make pretty
view0 = plot.getViewport(0)
yaxis = view0.getAxis("Y1")
yaxis.setReversed(FALSE)
precipCurve = plot.getCurve(precip)
precipCurve.setFillColor("blue")
precipCurve.setFillType("Above")
precipCurve.setLineVisible(FALSE)

#  Set the inflow and outflow colors
inflowCurve = plot.getCurve(inflow)
inflowCurve.setLineColor("magenta")
outflowCurve = plot.getCurve(outflow)
outflowCurve.setLineColor("purple")

plot.showPlot()
