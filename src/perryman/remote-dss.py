from hec.heclib.dss import HecDss
dssFileName    = "/var/tmp/tester.dss"
mustExist      = False
isRemote       = True
newFileVersion = 6

dssFile = HecDss.open(dssFileName, mustExist, isRemote, newFileVersion)

pathnames = dssFile.getPathnameList()
print("%d pathnames in file %s" % (len(pathnames), dssFileName))
dssFile.close()