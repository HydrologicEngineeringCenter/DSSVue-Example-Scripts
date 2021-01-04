#The GagePlot script is designed to produce a standard plot for a gage
# where there is both a stream flow gage and a precipitation gage.

# this script is run by passing arguments from RunGages.py
# To access arguments passed into the script you must include the following:
# import sys (sm = globals())
# Arguments are passed into a python script using a "name-space dictionary", which gives the keyword followed by a colon and then the parameter. Inside the script, the keyword will be replaced with the parameter. For example, in the GagePlot script, the name-space dictionary could be:
# "location" : "Glenfir", "version" : "OBS"
# Wherever the string location or version is in the script will
#  be substituted with GlenFir and Obs, respectively. 

from hec.script import Plot, MessageBox
from hec.heclib.dss import HecDss, DSSPathname
from hec.script.Constants import TRUE, FALSE
import java
import sys
# Access arguments
sm = globals()

#  "location" and "version" will be replaced with the arguments passed in

#  Retrieve data
try :
  #  If you wanted to use a relative time window, you could do something like:
  #  dssFile = HecDss.open("C:/temp/sample.dss", "T-30D, T")
  dssFile = HecDss.open(sys.argv[1] + "\\sample.dss", "01MAY1992 2400", "20MAY1992 2400")
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
plot.stayOpen()
#  If you wanted this to run in the background, you could add the following"
#  plot.setLocation(-10000, -10000)
#  plot.saveToPng("C:/temp/GagePlot.png")
#  plot.close()

