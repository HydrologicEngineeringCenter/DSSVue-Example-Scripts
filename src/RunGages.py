import sys
# Pass arguments and run Gageplot.py

#Set this to path for GagePlot.py
gplot = sys.argv[1] + "\\..\\src\\GagePlot.py"

glenFirArgs  = {"location" : "Glenfir", "version" : "OBS"}
execfile(gplot, {}, glenFirArgs)

madronArgs   = {"location" : "Oakville", "version" : "OBS"}
execfile(gplot, {}, madronArgs)

oakTreeArgs   = {"location" : "Walnut", "version" : "OBS"}
execfile(gplot, {}, oakTreeArgs)
