# name=ImportFolsomShef
# displayinmenu=true
# displaytouser=true
# displayinselector=true
from hec.script import *
from hec.dssgui import *
import java

ls = ListSelection.getMainWindow()
ls.setIsInteractive(1,0)  # Turn off popups
ls.open("C:/temp/myDb.dss")
ls.importShef("C:/temp/FolsomShefData.shef")

#ls.finish()  # Batch mode only


