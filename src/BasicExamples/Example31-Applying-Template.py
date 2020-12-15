import os# for getenv() & sep
from hec.script import Plot # for Plot class
from hec.heclib.dss import HecDss # for DSS class
thePlot = Plot.newPlot() # create a Plot
dssFile = HecDss.open("C:/temp/mydb.dss") # open the DSS file
flow = dssFile.get("/BASIN/LOC/FLOW/01NOV2002/1HOUR/OBS/")

#read a data set
thePlot.addData(flow) # add the data set
thePlot.showPlot()# show the plot
templateName = "myTemplate"# template base name
templateFileName =os.getenv("userprofile") \
+ os.sep \
+ "My Documents" \
+ os.sep \
+ templateName \
+ ".template"
thePlot.applyTemplate(templateFileName)# apply the template