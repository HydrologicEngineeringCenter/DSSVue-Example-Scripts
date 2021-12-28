from hec.dssgui import ListSelection

from hec.hecmath import DSS
dss = DSS.open(r"C:\project\DSSVue-Example-Scripts\data\sample.dss")
path = "/AMERICAN/FOLSOM/FLOW-RES IN/01JAN2006/1DAY/OBS/"
m = dss.read(path)
w = ListSelection.getMainWindow()
w.saveAs(m.getData())
#dss.saveAs(m.getData())
#1/0
w.finish()