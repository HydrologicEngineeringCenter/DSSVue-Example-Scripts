#Use ListSelection to open manual data entry dialog and save to mydb.dss

from hec.script import Plot, MessageBox
# from hec.io import TimeSeriesContainer
# from hec.io import PairedDataContainer
# from hec.hecmath import TimeSeriesMath
# from hec.hecmath import PairedDataMath
from hec.heclib.dss import HecDss, DSSPathname
from hec.dssgui import ListSelection
from hec.heclib.util import HecTime
import java
import sys



mw = ListSelection.getMainWindow()
mw.setIsInteractive(1,0)  # Turn off popups
mw.open(sys.argv[1] + "\\mydb.dss")

time = HecTime()
time.setCurrent()
time.setTime("0800")
time.addDays(-5)

mw.timeSeriesDataEntry("/GREEN/OAK/FLOW//1DAY/OBS", time.dateAndTime(4) )
# mw.finish()  # Batch mode only
