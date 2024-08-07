from hec.script import Plot
from hec.heclib.dss import HecDss 
from hec.hecmath import PlotUtilities
from hec.script.Constants import TRUE, FALSE

#startTime="01Sep2021 2400"
#endTime="17Sep2021 2400"
dss = HecDss.open(R"C:\project\DSSVue-Example-Scripts\src\Y-axis\Savannah_CWMS-SHEF-data.dss")#,startTime,endTime)

HART1 = dss.get("/SAVANNAH/HARTWELL/ELEV-POOL//1HOUR/OBS/")
RUSS1 = dss.get("/SAVANNAH/RUSSELL/ELEV-POOL//1HOUR/OBS/")

#G2dDialog
p=Plot.newPlot("Title")

p.addData(HART1)
p.addData(RUSS1)


p.showPlot()

print(HART1)
c = p.getGlyph("/SAVANNAH/HARTWELL/ELEV-POOL//1HOUR/OBS/")
print(c)
print(type(c))  #hec.gfx2d.TimeSeriesGlyph'
c.setLegendItemsVisible(0)

#1/0
vports = p.getViewports()
#print(vports)
#G2dLine1 = PlotUtilities.getCurve(p, HART1.toString())
#print(G2dLine1)
#c=p.getCurve("/SAVANNAH/HARTWELL/ELEV-POOL//1HOUR/OBS/")
#c=p.getCurve(HART1.getPath())
#print(c)

#c = myPlot.getCurve("/SAVANNAH/HARTWELL/ELEV-POOL/01JAN2019/1HOUR/OBS/")
#print(c)
#c.setLegendItemsVisible(TRUE)
#c.isLegendItemsVisible(TRUE)
print(FALSE)
#g.setLineLabelVisible(FALSE)
p.repaint()
p.stayOpen()
