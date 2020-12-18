#Importing shef files to DSS
from hec.script import Plot, MessageBox
from hec.heclib.dss import HecDss, DSSPathname
from hec.dssgui import ListSelection
import java
import sys

ls = ListSelection.getMainWindow()
ls.setIsInteractive(1,0)  # Turn off popups
ls.open("c:/temp/import.dss")
ls.importShef("c:/temp/FolsomShefData.shef")
#ls.finish()  # Batch mode only


