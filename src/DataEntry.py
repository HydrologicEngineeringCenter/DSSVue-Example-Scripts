# name=DataEntry
# displayinmenu=true
# displaytouser=true
# displayinselector=true
from hec.script import *
from hec.dssgui import *
from hec.heclib.util import *
import java

mw = ListSelection.getMainWindow()
mw.setIsInteractive(1,0)  # Turn off popups
mw.open("C:/temp/mydb.dss")

time = HecTime()
time.setCurrent()
time.setTime("0800")
time.addDays(-5)

mw.timeSeriesDataEntry("/GREEN/OAK/FLOW//1DAY/OBS", time.dateAndTime(4) )
# mw.finish()  # Batch mode only
