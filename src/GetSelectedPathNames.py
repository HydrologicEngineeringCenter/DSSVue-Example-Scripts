from hec.dssgui import ListSelection

listSelection = ListSelection.getMainWindow()

count = listSelection.getNumberSelectedPathnames()
print(count)

vector = listSelection.getSelectedPaths()
for p in vector:
 print(p)
