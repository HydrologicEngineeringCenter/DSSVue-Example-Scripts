#Used to pass arguments and run Gageplot.py

#Set this to path for GagePlot.py
gplot = "C:/Path/To/GagePlot.py"

glenFirArgs  = {"location" : "Glenfir", "version" : "OBS"}
execfile(gplot, {}, glenFirArgs)

madronArgs   = {"location" : "Oakville", "version" : "OBS"}
execfile(gplot, {}, madronArgs)

oakTreeArgs   = {"location" : "Walnut", "version" : "OBS"}
execfile(gplot, {}, oakTreeArgs)
