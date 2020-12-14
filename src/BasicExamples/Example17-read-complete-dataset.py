from hec.script import Plot,MessageBox
from hec.heclib.dss import HecDss
import java

try :
  myDss = HecDss.open("C:/temp/sample.dss")
  flow = myDss.get("/MISSISSIPPI/ST. LOUIS/FLOW//1DAY/OBS/", 1)

  if flow.numberValues == 0 :
    MessageBox.showError("No Data", "Error")
  else :
    plot = Plot.newPlot("Mississippi")
    plot.addData(flow)
    plot.showPlot()
    plot.stayOpen()
except Exception, e :
    MessageBox.showError(' '.join(e.args), "Python Error")
except java.lang.Exception, e :
    MessageBox.showError(e.getMessage(), "Error")
finally :
  myDss.done()