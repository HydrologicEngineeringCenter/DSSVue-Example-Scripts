#Importing shef files to DSS
from hec.script import Plot, MessageBox
# from hec.io import TimeSeriesContainer
# from hec.io import PairedDataContainer
# from hec.hecmath import TimeSeriesMath
# from hec.hecmath import PairedDataMath
from hec.heclib.dss import HecDss, DSSPathname
from hec.dssgui import ListSelection
import java
import sys

ls = ListSelection.getMainWindow()
ls.setIsInteractive(1,0)  # Turn off popups
ls.open(sys.argv[1] + "\\myDb.dss")
ls.importShef(sys.argv[1] + "\\FolElev.shef")
ls.importShef(sys.argv[1] + "\\FolFlowIn.shef")

#ls.finish()  # Batch mode only


