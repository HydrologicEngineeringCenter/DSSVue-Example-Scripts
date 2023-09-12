from hec.script import Plot
from hec.heclib.dss import HecDss 

def setupYAxis(plot,viewPortIndex,label,min,max):
    vp = plot.getViewport(viewPortIndex)
    yaxis = vp.getAxis("Y1")
    yaxis.setLabel(label)
    yaxis.setScaleLimits(min,max)
#    print "viewPort:"+label,vp,"yaxis: ",yaxis


startTime="01Sep2021 2400"
endTime="17Sep2021 2400"
dss = HecDss.open(R"C:\project\DSSVue-Example-Scripts\src\Y-axis\Savannah_CWMS-SHEF-data.dss",startTime,endTime)

HART1 = dss.get("/SAVANNAH/HARTWELL/ELEV-POOL/01JAN2019/1HOUR/OBS/")
RUSS1 = dss.get("/SAVANNAH/RUSSELL/ELEV-POOL/01JAN2019/1HOUR/OBS/")
THUR1 = dss.get("/SAVANNAH/THURMOND/ELEV-POOL/01JAN2019/1HOUR/OBS/")
# need to outsmart gfx2d -- make units differnet so there are separate y-axis values.
# another workaround reported:is to use setAxisName and setAxisLabel after defining the viewport
#
HART1.units +="1"
RUSS1.units +="2"
THUR1.units +="3"

myPlot=Plot.newPlot("PoolPlots")
layout = Plot.newPlotLayout()
Hartwell = layout.addViewport(34.)
Russell = layout.addViewport(33.)
Thurmond = layout.addViewport(33.)
print layout.getViewports()
print Hartwell,Russell,Thurmond
Hartwell.addCurve("Y1", HART1)
Russell.addCurve("Y1", RUSS1)
Thurmond.addCurve("Y1", THUR1)

myPlot.configurePlotLayout(layout)
myPlot.showPlot()
setupYAxis(myPlot,0,"Hartwell",655.,665.)
setupYAxis(myPlot,1,"Russell",470.,480.)
setupYAxis(myPlot,2,"Thurmond",312.,335)

myPlot.stayOpen()
