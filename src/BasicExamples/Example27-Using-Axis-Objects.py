
from hec.script import Plot# for Plot class
from hec.heclib.dss import HecDss# for DSS class
thePlot = Plot.newPlot()# create a Plot
dssFile = HecDss.open("mydb.dss")# open the DSS file
flow = dssFile.get("/BASIN/LOC/FLOW/01NOV2002/1HOUR/OBS/")

#read a data set
thePlot.addData(flow) # add the data set
thePlot.showPlot()# show the plot
viewport0 = thePlot.getViewport(0)# get the first Viewport
yaxis = viewport0.getAxis("Y1")# get the Y1 axis
yaxis.setScaleLimits(0., 25000.) # set the scale
yaxis.zoomByFactor(.5)# zoom in