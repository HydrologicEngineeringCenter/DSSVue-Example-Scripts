from hec.heclib.dss import HecDss, DSSPathname
import os


def getDssFiles(dir):
 rval=[]
 
 dssFileNames = os.listdir(dir)
 for f in dssFileNames: 
    if f.endswith(".dss"):
        fn = dir+"\\"+f
        rval.append(fn)
 return rval
 
 
dir = R"C:\project\DSSVue-Example-Scripts\data\Jeremy"
files = getDssFiles(dir)
outputFileName = R"C:\tmp\ua_co_combined.dss"

if os.path.exists(outputFileName):
  os.remove(outputFileName)

outputDss = HecDss.open(outputFileName)

for f in files:
	dss = HecDss.open(f)
	paths = dss.getCondensedCatalog()
#	print(paths)
	for cr in paths:
	  p = DSSPathname(cr.toString())
	  p.setDPart("")
	  ep = p.getEPart()
	  # if epart starts with IR-, print warning, skip
	  if ep.upper().startswith("IR-"):
	    print("Warning: path is irregular" + p.toString())
	    continue
	  print(p.toString())
	  tsc = dss.get(p.toString())
	  
	  outputDss.put(tsc)
	
	
	

