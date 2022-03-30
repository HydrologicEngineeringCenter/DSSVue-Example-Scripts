#!/awips2/python/bin/python

#########################################################################################################
# This file converts output xml files from CHPS and converts them to DSS for use in the HEC-RAS model   #
# The batch list of CHPS files to convert are read from a file named "chps2dss_convert_batch_list"	#
# These files are passed through HEC-DSSVue and output as DSS files by using "hec-dssvue.sh"		#
# The DSS output files are placed where specified in the file "chps2dss_convert_batch_list" file	#
# - MBRFC - jmt 05/24/17"										#
#													#
#########################################################################################################

# name=Import Calb Card
# description=Import Calibration Card
# displaytouser=false
from hec.plugins.dssvue.piXml import *
from hec.script import *
from hec.heclib.dss import *
from hec.heclib.util import *
from hec.dssgui import *
from hec.io import *
import java
import os    # needed to get the latest file from lmrfc 
import glob  # needed to get the latest file from lmrfc 
from shutil import copyfile  #needed to copy archived lmrfc file, rename it for conversion, then delete it



####################     CHANGE THESE FOLDERS AND FILES AS NECESSARY      ###################################################################
#############################################################################################################################################
# Gets the file with the list of CHPS files to convert and where to put the DSS output files
inpFile='/awips/hydroapps/lx/rfc/lmrfc/hec-dssvue201_chps_beta/HEC-DSSVue/scripts/chps2dss_convert_batch_list_miss'  # list of CHPS export files to convert and output names
lmrfcDir='/awips/chps_share/data/export/hecras_pixml'     # location of the lmrfc xml files for HEC-RAS
lmrfcOutFile='/awips/chps_share/data/export/hecras_pixml/HEC-RAS_miss.dss'    # name and location of converted lmrfc dss files
tempXML = '/awips/rep/lx/rfc/lmrfc/hec-dssvue201_chps_beta/HEC-DSSVue/scripts/templmrfc.xml'
#############################################################################################################################################

# runs the DSSVue conversion script
def convert_CHPS2DSS(inFile,outFile):
    # Opens an empty DSS file to dump the converted time series
    ls = ListSelection.getMainWindow()
    ls.setIsInteractive(1,0)     #Turn off popups
    ls.open(outFile)

    # create an instance of PiXmlTsImport
    pixml = PiXmlTsImport()

    # open and read pi.xml file
    chpsfile = java.io.File(inFile)
    pixml.startImport(chpsfile)

    # get the vector of time series containers and write to dss
    piTs = pixml.getData()
    ls.saveData(piTs)

    # maybe get error messages (should be empty if no problems)
    errorMess = pixml.getMessage()

# Reads the batch list from the file and gets lates lmrfc file
def inOut(listFile,lmrfcIn,lmrfcOut,tempFile):
    inOutDict = {}
    # Reads the batch list from the file
    #for l in open(listFile).readlines()[1:]:
	#fIn, fOut = l.split(',')
	#fOut = fOut.rstrip('\n')
	#inOutDict[fIn] = fOut

    # Gets the latest lmrfc file
    newest = max(glob.iglob(lmrfcIn + '/*HECRAS_pixml_export.temp*'), key=os.path.getctime)   # finds the newest xml file from lmrfc
    copyfile(newest,tempFile)
    fIn = tempFile
    fOut = lmrfcOut
    inOutDict[fIn] = fOut
    
    return inOutDict

#######   Main program  ##########
convertFiles = inOut(inpFile,lmrfcDir,lmrfcOutFile,tempXML)

for k,v in convertFiles.iteritems():
    convert_CHPS2DSS(k,v)

os.remove(tempXML)   # Remove temporary xml file








