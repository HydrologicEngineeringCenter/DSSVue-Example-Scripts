from hec.script import HecDss
import jarray
from hec.heclib.grid import GridUtilities


########################################
#  Set file names for input and output #
########################################

inDssFileName = "C:/Class/DSS/Gridded Data/MPE.dss"
outDssFileName = "C:/Class/DSS/Gridded Data/MPEsum.dss"

##################################################
#  Set paths for retrieving one day of MPE grids #
##################################################

gridPaths = [
'/HRAP/NCRFC/PRECIP/19JUL2017:0000/19JUL2017:0100/MPE/',
'/HRAP/NCRFC/PRECIP/19JUL2017:0100/19JUL2017:0200/MPE/',
'/HRAP/NCRFC/PRECIP/19JUL2017:0200/19JUL2017:0300/MPE/',
'/HRAP/NCRFC/PRECIP/19JUL2017:0300/19JUL2017:0400/MPE/',
'/HRAP/NCRFC/PRECIP/19JUL2017:0400/19JUL2017:0500/MPE/',
'/HRAP/NCRFC/PRECIP/19JUL2017:0500/19JUL2017:0600/MPE/',
'/HRAP/NCRFC/PRECIP/19JUL2017:0600/19JUL2017:0700/MPE/',
'/HRAP/NCRFC/PRECIP/19JUL2017:0700/19JUL2017:0800/MPE/',
'/HRAP/NCRFC/PRECIP/19JUL2017:0800/19JUL2017:0900/MPE/',
'/HRAP/NCRFC/PRECIP/19JUL2017:0900/19JUL2017:1000/MPE/',
'/HRAP/NCRFC/PRECIP/19JUL2017:1000/19JUL2017:1100/MPE/',
'/HRAP/NCRFC/PRECIP/19JUL2017:1100/19JUL2017:1200/MPE/',
'/HRAP/NCRFC/PRECIP/19JUL2017:1200/19JUL2017:1300/MPE/',
'/HRAP/NCRFC/PRECIP/19JUL2017:1300/19JUL2017:1400/MPE/',
'/HRAP/NCRFC/PRECIP/19JUL2017:1400/19JUL2017:1500/MPE/',
'/HRAP/NCRFC/PRECIP/19JUL2017:1500/19JUL2017:1600/MPE/',
'/HRAP/NCRFC/PRECIP/19JUL2017:1600/19JUL2017:1700/MPE/',
'/HRAP/NCRFC/PRECIP/19JUL2017:1700/19JUL2017:1800/MPE/',
'/HRAP/NCRFC/PRECIP/19JUL2017:1800/19JUL2017:1900/MPE/',
'/HRAP/NCRFC/PRECIP/19JUL2017:1900/19JUL2017:2000/MPE/',
'/HRAP/NCRFC/PRECIP/19JUL2017:2000/19JUL2017:2100/MPE/',
'/HRAP/NCRFC/PRECIP/19JUL2017:2100/19JUL2017:2200/MPE/',
'/HRAP/NCRFC/PRECIP/19JUL2017:2200/19JUL2017:2300/MPE/',
'/HRAP/NCRFC/PRECIP/19JUL2017:2300/19JUL2017:2400/MPE/']

#####################################################
#  Retrive a data container from the first DSS path #
#####################################################
inDSS = HecDss.open(inDssFileName)
dataContainer = inDSS.get(gridPaths[0])

###########################################################
#  Pull a GridData object from the container.             #
#  This grid will hold the first hour's MPE grid.         #
#  The same grid will be used to hold the sum of the set. #
###########################################################
outData = dataContainer.getGridData()

# create java array of integers (length = 1) to hold retrieve method staus
status = jarray.array([-9999], 'i')

################################################
#  Loop over the remaining paths.              #
#  Add the contents of each new grid to the    #
#   running total in outData.                  #
################################################
for path in gridPaths[1:]:
    dataContainer = inDSS.get(path)
    nextGrid = dataContainer.getGridData()
    outData = GridUtilities.gridAdd(outData, nextGrid, status)

#########################################
#  Adjust the dates in the grid header. #
#########################################
outData.getGridInfo().setGridTimes("19JUL2017:0000", "19JUL2017:2400")

###########################################
#  Write the grid to the output DSS file. #
###########################################
GridUtilities.storeGridToDss(outDssFileName, '/HRAP/NCRFC/PRECIP/19JUL2017:0000/19JUL2017:2400/MPE/', outData)
inDSS.close()

print "\nMPE sum completed!"
