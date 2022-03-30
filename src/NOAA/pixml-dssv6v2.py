# name=PiXML
# displayinmenu=true
# displaytouser=true
# displayinselector=true
import datetime, sys
from hec.heclib.util import HecTime
from hec.hecmath import DSS, TimeSeriesMath
from hec.io import TimeSeriesContainer
from hec.script import Constants
from java.lang import Math
# from hec.script import *
# from hec.heclib.dss import *
# import java
from hec.plugins.dssvue.piXml import PiXmlTsImport
from java.io import File
from hec.dssgui      import ListSelection
from hec.heclib.dss  import HecDss
from hec.heclib.util import Heclib

Heclib.zset("DSSV","",6)
# dssFile = "c:\py\piXML.dss"
dssFile = "forecast2.dss"
# dssFile = DSSfl
dss = HecDss.open(dssFile)

pi = PiXmlTsImport()
# piFile= File("NAEFS_pixml")
piFile= File("HECRAS_NAEFS_pixml_export.20211201163854")
# piFile= pixmlFl
pi.startImport(piFile)
dc = pi.getData()

for path in dc:
	dss.put(path)
dss.close()
