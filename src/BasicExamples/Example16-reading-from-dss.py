from javax.swing import JOptionPane
from hec.heclib.dss import HecDss
from hec.script import Plot
import java

try : 
  try :
    myDss = HecDss.open("C:/temp/sample.dss")
    flow = myDss.get("/RUSSIAN/NR UKIAH/FLOW/01MAR2006/1HOUR//")
    plot = Plot.newPlot("Russian River at Ukiah")
    plot.addData(flow)
    plot.showPlot()
  except Exception, e :
    JOptionPane.showMessageDialog(None, ' '.join(e.args), "Python Error", JOptionPane.ERROR_MESSAGE)
  except java.lang.Exception, e :
    MessageBox.showError(e.getMessage(), "Java Error")
finally :
  myDss.done()
