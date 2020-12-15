from hec.script import Plot
from hec.heclib.dss import HecDss
theFile = HecDss.open("myFile.dss")# open myFile.dss
precipPath = "/BASIN/LOC/FLOW/01NOV2002/1HOUR/OBS/"
stagePath = "/BASIN/LOC/FLOW/01NOV2002/1HOUR/OBS/"
flowPath = "/BASIN/LOC/FLOW/01NOV2002/1HOUR/OBS/"
precipData = theFile.get(precipPath)# read the precip
stageData = theFile.get(stagePath)# read the stage
flowData = theFile.get(flowPath)# read the flow
thePlot = Plot.newPlot()# create a new Plot
layout = Plot.newPlotLayout()# create a new PlotLayout
topView = layout.addViewport(30)# get the top viewport
bottomView = layout.addViewport(70)# get the bottom viewport
topView.addCurve("Y1", precipData)# add the precip to top
bottomView.addCurve("Y1", stageData)# add the stage to bottom
bottomView.addCurve("Y2", flowData)# add the flow to bottom
thePlot.configurePlotLayout(layout)# configure the plot
thePlot.showPlot()# show the plot