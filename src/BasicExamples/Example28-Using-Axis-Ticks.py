from hec.script import Plot
from hec.script.Constants import TRUE, FALSE
from hec.heclib.dss import HecDss
thePlot = Plot.newPlot() # create a Plot
dssFile = HecDss.open("c:/temp/mydb.dss") # open the DSS file
flow = dssFile.get("/BASIN/LOC/FLOW/01NOV2002/1HOUR/OBS/")

#read a data set
thePlot.addData(flow) # add the data set
thePlot.showPlot()# show the plot
viewport0 = thePlot.getViewport(flow)# get the viewport for the #flow data set
yAxisTics = viewport0.getAxisTics("Y1")# get the axis tics for the #Viewport
yAxisTics.setMinorTicsVisible(TRUE) # tell axis tics to show tics