# name=RunGages
# displayinmenu=false
# displaytouser=false
# displayinselector=true
from hec.script import *

glenFirArgs  = {"location" : "Glenfir", "version" : "OBS"}
execfile("C:/HecDSSVueDev/HecDssVue/scripts/GagePlot.py", {}, glenFirArgs)

madronArgs   = {"location" : "Madron", "version" : "OBS"}
execfile("C:/HecDSSVueDev/HecDssVue/scripts/GagePlot.py", {}, madronArgs)

oakTreeArgs   = {"location" : "Madron", "version" : "OBS"}
execfile("C:/HecDSSVueDev/HecDssVue/scripts/GagePlot.py", {}, oakTreeArgs)
