from hec.script import Plot
from hec.script.Constants import TRUE, FALSE
from hec.heclib.dss import HecDss
theFile = HecDss.open(r"C:\project\DSSVue-Example-Scripts\data\sample.dss")
thePath = "/AMERICAN/FOLSOM/FLOW-RES IN/01JAN2006/1DAY/OBS/"
flowDataSet = theFile.get(thePath)	# read a path name
thePlot = Plot.newPlot()	# create the plot
thePlot.addData(flowDataSet)	# add the flow data set to the plot
thePlot.showPlot()	# show the plot
viewport0=thePlot.getViewport(0)	# get the first viewport
viewport0.setMinorGridYColor("black")	# set the viewport's minor Y grid to black
viewport0.setMinorGridYVisible(TRUE) 	# tell the minor Y grid to display
thePlot.stayOpen()