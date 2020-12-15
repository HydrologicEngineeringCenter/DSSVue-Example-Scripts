from hec.script import Plot
from hec.script.Constants import TRUE, FALSE
from hec.heclib.dss import HecDss
thePlot = Plot.newPlot() # create a Plot
dssFile = HecDss.open("C:/temp/mydb.dss") # open the DSS file
stage = dssFile.get("/BASIN/LOC/FLOW/01NOV2002/1HOUR/OBS/")

#read a data set
thePlot.addData(stage) # add the data set
thePlot.showPlot()# show the plot
stageCurve = thePlot.getCurve(stage)# get the stage curve
stageCurve.setSymbolsAutoInterval(TRUE)# turn on symbols auto skip