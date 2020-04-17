# name=Glenfir
# displayinmenu=false
# displaytouser=false
# displayinselector=true
from hec.script import *
from hec.hecmath import *
from hec.script.Constants import TRUE, FALSE
import java

dssFile = HecDss.open("C:/temp/sample.dss", "01MAY1992 2400", "20MAY1992 2400")
flowPath = "/GREEN RIVER/GLENFIR/FLOW//1HOUR/OBS/"
precipPath = "/GREEN RIVER/GLENFIR/PRECIP-INC//1HOUR/OBS/"
precip = dssFile.get(precipPath)
flow = dssFile.get(flowPath)

plot = Plot.newPlot("Glenfir")
layout = Plot.newPlotLayout()
topView = layout.addViewport(15.)
bottomView = layout.addViewport(85.)

topView.addCurve("Y1", precip)
bottomView.addCurve("Y1", flow)
plot.configurePlotLayout(layout)
plot.setSize(600, 500)

plot.setPlotTitleText("Glenfir")
tit = plot.getPlotTitle()
tit.setFont("Arial Black")
tit.setFontSize(18)
plot.setPlotTitleVisible(TRUE)

plot.showPlot()

panel = plot.getPlotpanel()
panel.setHorizontalViewportSpacing(0)

view0 = plot.getViewport(0)
yaxis = view0.getAxis("Y1")
yaxis.setReversed(FALSE)

precipCurve = plot.getCurve(precip)
precipCurve.setFillColor("blue")
precipCurve.setFillType("Above")
precipCurve.setLineColor("blue")

flowCurve = plot.getCurve(flow)
flowCurve.setLineColor("darkgreen")
flowCurve.setLineWidth(2.)

plot.setLegendLabelText(flow, "Flow")
plot.setLegendLabelText(precip, "Rainfall")

