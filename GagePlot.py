# name=GagePlot
# displayinmenu=false
# displaytouser=false
# displayinselector=false
# Both location=name version=ver must be defined as arguments
# To run:  GagePlot {"location" : "Glenfir", "version" : "OBS"}
# e.g.,
#  glenFirArgs  = {"location" : "Glenfir", "version" : "OBS"}
#  execfile("C:/HecDSSVueDev/HecDssVue/scripts/GagePlot.py", {}, glenFirArgs)

from hec.script import *
from hec.heclib.dss import *
import sys
import java
from hec.script.Constants import TRUE, FALSE

# Access arguments
sm = globals()

#  "location" and "version" will be replaced with the arguments passed in

#  Retrieve data
try :
  #  If you wanted to use a relative time window, you could do something like:
  #  dssFile = HecDss.open("C:/temp/sample.dss", "T-30D, T")
  dssFile = HecDss.open("C:/temp/sample.dss", "01MAY1992 2400", "20MAY1992 2400")
  flowPath = "/GREEN RIVER/" + location + "/FLOW//1HOUR/OBS/"
  precipPath = "/GREEN RIVER/" + location + "/PRECIP-INC//1HOUR/OBS/"
  precip = dssFile.get(precipPath)
  flow = dssFile.get(flowPath)
except java.lang.Exception, e :
  MessageBox.showError(e.getMessage(), "Error reading data")

# Create plot and viewports
plot = Plot.newPlot()
layout = Plot.newPlotLayout()
topView = layout.addViewport(15.)
bottomView = layout.addViewport(85.)

#  Add data
topView.addCurve("Y1", precip)
bottomView.addCurve("Y1", flow)
plot.configurePlotLayout(layout)
plot.setSize(600, 500)

#  Add title
plot.setPlotTitleText(location)
tit = plot.getPlotTitle()
tit.setFont("Arial Black")
tit.setFontSize(18)
plot.setPlotTitleVisible(TRUE)

#  This actually creates the plot - cannot access any components until done
plot.showPlot()

#  Now we can change components
panel = plot.getPlotpanel()
#  Remove space between viewports
panel.setHorizontalViewportSpacing(0)

#  Invert the precip
view0 = plot.getViewport(0)
yaxis = view0.getAxis("Y1")
yaxis.setReversed(FALSE)

#  Make the precip pretty
precipCurve = plot.getCurve(precip)
precipCurve.setFillColor("blue")
precipCurve.setFillType("Above")
precipCurve.setLineColor("blue")

#  Make the flow pretty
flowCurve = plot.getCurve(flow)
flowCurve.setLineColor("darkgreen")
flowCurve.setLineWidth(2.)

#  Set the legend labels
plot.setLegendLabelText(flow, "Flow")
plot.setLegendLabelText(precip, "Rainfall")

# Done (should look like we want now)

#  If you wanted this to run in the background, you could add the following"
#  plot.setLocation(-10000, -10000)
#  plot.saveToPng("C:/temp/GagePlot.png")
#  plot.close()

