#Importing shef files to DSS
from hec.script import Plot, MessageBox
# from hec.io import TimeSeriesContainer
# from hec.io import PairedDataContainer
# from hec.hecmath import TimeSeriesMath
# from hec.hecmath import PairedDataMath
from hec.heclib.dss import HecDss, DSSPathname
from hec.dssgui import ListSelection
import java

ls = ListSelection.getMainWindow()
ls.setIsInteractive(1,0)  # Turn off popups
ls.open("C:/temp/myDb.dss")
ls.importShef("C:/temp/FolElev.shef")
ls.importShef("C:/temp/FolFlowIn.shef")

#ls.finish()  # Batch mode only


