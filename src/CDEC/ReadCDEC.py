from hec.heclib.dss import HecDss

from hec.plugins.cdec import CdecControlFrame
import java

fileName = R"C:\project\DSSVue-Example-Scripts\src\CDEC\Oroville.dss"
cdecName = R"C:\project\DSSVue-Example-Scripts\src\CDEC\Oroville.cdec"
tw = "T-360D, T+1D"

dss = HecDss.open(fileName,tw)
cdec = CdecControlFrame(dss)

cdec.loadStations(cdecName)
status = cdec.retrieveData()   
print(status)

sys.stdin.readline()
