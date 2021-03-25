#from hec.script import Plot, MessageBox
#from hec.heclib.dss import HecDss, DSSPathname
from hec.dssgui import ListSelection

import java
ls = ListSelection.getMainWindow()
ls.setIsInteractive(1,0) # Turn off popups
ls.open("C:/temp/myDb.dss")
ls.importShef("C:/temp/FolsomShefData.shef")
#ls.finish() # Batch mode only
 