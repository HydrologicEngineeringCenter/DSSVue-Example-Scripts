from hec.plugins.dssvue.piXml import PiXmlTsImport
from hec.dssgui import ListSelection
from java.io import File

def convert_CHPS2DSS(inFile,outFile):
    ls = ListSelection.getMainWindow()
    ls.setIsInteractive(1,0)     #Turn off popups
    ls.open(outFile)
    pixml = PiXmlTsImport()
    chpsfile = File(inFile)
    pixml.startImport(chpsfile)
    piTs = pixml.getData()
    ls.saveData(piTs)
    errorMess = pixml.getMessage()

pixmlInput ="pixml-sample.xml"
dssFile = "pi-xml-import-test.dss"
convert_CHPS2DSS(pixmlInput,dssFile)


