from hec.script import Plot	# for Plot class
from hec.script.Constants import TRUE, FALSE
from hec.heclib.dss import HecDss	# for DSS class
theFile = HecDss.open("myFile.dss")	# open myFile.dss
thePath = "/BASIN/LOC/FLOW/01NOV2002/1HOUR/OBS/"
flowDataSet = theFile.read(thePath)	# read a path name
thePlot = Plot.newPlot()	# create a new Plot
thePlot.addData(flowDataSet)	# add the flow data
viewport0=thePlot.getViewport(0)	# get the first Viewport
viewport0.setBackground("lightgray")	# set the Viewport's bg
viewport0.setBackgroundVisible(TRUE) 	# tell Viewport to draw bg
marker = AxisMarker()	# create a new marker
marker.axis = "Y" 	# set the axis
marker.value = "20000" 	# set the value
marker.labelText = "Damaging Flow" 	# set the text
marker.labelColor = "red" 	# set the text color
marker.lineColor = "red" 	# set the line color
marker.fillColor = "red" 	# set the fill color
marker.fillType = "above" 	# set the fill type
maker.fillPattern = "diagonal cross" 	# set the fill pattern
viewport0.addAxisMarker(marker) 	# add the marker to the
	                # viewport
