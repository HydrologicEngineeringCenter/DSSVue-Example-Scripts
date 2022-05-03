from hec.plugins.dssvue.piXml import PiXmlTsExport
from java.io import File
from java.util import Vector
from hec.heclib.dss  import HecDss

dssFilename = R"C:\project\DSSVue-Example-Scripts\data\sample.dss"
pixmlFilename = R"C:\tmp\out.pi.txt"

path="//SACRAMENTO/PRECIP-INC/01JAN1877/1DAY/OBS/"

dss = HecDss.open(dssFilename)
dc = dss.get(path)

# PiXmlTsExport expects Vector array (Vector[])
v = Vector()
v2 = Vector()
v2.add(dc)
v.add(v2)

pi = PiXmlTsExport(v)
piFile= File(pixmlFilename)
pi.startExport(piFile)
