from hec.script import Plot
from hec.heclib.dss import HecDss
thePlot = Plot.newPlot()# create a Plot
dssFile = HecDss.open("C:/temp/mydb.dss")# open the DSS file
flow = dssFile.get("/BASIN/LOC/FLOW/01NOV2002/1HOUR/OBS/")

#read a data set
thePlot.addData(flow) # add the data set
thePlot.showPlot()# show the plot
viewport0 = thePlot.getViewport(0)# get the first viewport
yaxislabel = viewport0.getAxisLabel("Y1")# get the Y1 axis label
yaxislabel.setForeground("blue")# set the Y1 axis label text to blue