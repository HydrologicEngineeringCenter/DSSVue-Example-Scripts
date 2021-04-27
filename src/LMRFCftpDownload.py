from ftplib import FTP
import ftplib
import datetime
import gzip
import shutil
import os
from hec.heclib.dss import HecDss, DSSPathname
 ##################################################################################  
def downloadGz(workingDir, gzFileName):
    gzFPath = workingDir + gzFileName
    locf = open(gzFPath,'wb')
    ftp.retrbinary('RETR ' + f, locf.write, 8*1024)
    locf.close()
    print ("Downloaded "+ f + " to " + workDir)
    return gzFPath

def decompressGz(gzPath):
        dssF = os.path.splitext(gzPath)[0]
        with gzip.open(gzPath, 'r') as f_in, open(dssF, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
        return dssF
            
def mergeDssRecords(src, dest):
    try:
        srcHecDss = HecDss.open(src)
        destHecDss = HecDss.open(dest)
        srcTsMath = srcHecDss.read("/JNEL1/BLACK-JONESVILLE/FLOW//6Hour//")
        destTsMath = destHecDss.read("/JNEL1/BLACK-JONESVILLE/FLOW//6Hour//")
        tsMerged = destTsMath.mergeTimeSeries(srcTsMath)
        srcHecDss.write(tsMerged)
        srcHecDss.done()
        destHecDss.done()       
    except Exception, e:
        print(e)
#############################################################################            
workDir = "C:\\Temp\\"
dxDSS = workDir+"Jonesville.dss"

ftp = FTP('tgftp.nws.noaa.gov')
ftp.login()             
ftp.cwd('/data/rfc/lmrfc/misc')
  
today = datetime.datetime.now()
dateStr = today.strftime("%Y%m%d")

files = []
try:
    files = ftp.nlst()
except ftplib.error_perm, resp:
    if str(resp) == "55 No files found":
        print "No files in this directory"
    else:
        raise
    
for f in files:
    if dateStr in f and "dss" in f:
        gzFPath = downloadGz(workDir, f)
        dssF = decompressGz(gzFPath)
        mergeDssRecords(dssF, dxDSS)  
    else:
        print "Skipping "+f
ftp.quit()
