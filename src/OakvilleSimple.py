# Simple Plotting Example
# Generally, graphics scripts may be broken into five segments; 
# 1) Retrieve the data; 
# 2) Initialize the plot; 
# 3) Bring the plot into existence with showPlot(); 
# 4) Change the plot; and 
# 5) Save the plot to file and close.
# Most people are tripped up with the function showPlot(). 
# This function puts all the parts together and creates the plot. 
# One would think that this would be called at the end of the script, 
# but to the contrary, it needs to be called near the beginning.
# For example, you can not change or set a curve's color until the curve exists, and the showPlot() function is what creates curves. Scripting is emulating the steps that you would do interactively; it is not a command language.
# HecDss uses exceptions for error processing, such as indicating missing data. You need to use try: except loops to catch errors, otherwise an exception message will be written to the output and that exception may not be very clear.
from hec.script import Plot, MessageBox
from hec.heclib.dss import HecDss, DSSPathname
import java
import sys

#  Open the file and get the data
try :
  dssFile = HecDss.open(sys.argv[1] + "\\sample.dss")
  airTemp = dssFile.get("/GREEN RIVER/OAKVILLE/AIRTEMP/01MAY1992/1HOUR/OBS/")
  outflow = dssFile.get("/GREEN RIVER/OAKVILLE/FLOW-RES OUT/01MAY1992/1HOUR/OBS/")
  dssFile.done()
except java.lang.Exception, e :
  #  Take care of any missing data or errors
   MessageBox.showError(e.getMessage(), "Error reading data")

#  Initialize the plot and add data
plot = Plot.newPlot("Oakville")
plot.addData(airTemp)
plot.addData(outflow)

#  Create plot
plot.setSize(600,600)
plot.setLocation(100,100)
plot.showPlot()

#  Change the plot
outCurve = plot.getCurve(outflow)
outCurve.setLineColor("darkgreen")

#  Save the plot and close
plot.saveToPng(sys.argv[2] + "\\Oakville.png")
#plot.close()  #  Do this if you only want the plot as a .png and not on screen
