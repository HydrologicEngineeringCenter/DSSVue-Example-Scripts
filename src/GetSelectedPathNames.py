from hec.dssgui import ListSelection
from hec.heclib.dss import DSSPathname

listSelection = ListSelection.getMainWindow()

count = listSelection.getNumberSelectedPathnames()
print(count)
vector = listSelection.getSelectedPaths()
for p in vector:
 print(p)
 print(type(p))


 ds = listSelection.getSelectionList()     # DataReferenceSet
 dr = ds.get(0) # get first selection (DataReference)
print(dr.pathname())
dssPath = DSSPathname(dr.pathname())  

title = dssPath.bPart()
print(title)
