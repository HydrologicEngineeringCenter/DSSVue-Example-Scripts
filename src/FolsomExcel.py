#from hec.script import *
from hec.heclib.dss import HecDss
from hec.dataTable import HecDataTableToExcel
import java
import sys
# Open the file and get the data
try:
 dssFile = HecDss.open("c:/temp/sample.dss", "10MAR2006 2400, 09APR2006 2400")
 precip = dssFile.get("/AMERICAN/FOLSOM/PRECIPBASIN/01JAN2006/1DAY/OBS/")
 stor = dssFile.get("/AMERICAN/FOLSOM/ STOR-RES EOP/01JAN2006/1DAY/OBS/")
 topcon = dssFile.get("/AMERICAN/FOLSOM/TOP CON STOR/01JAN2006/1DAY/OBS/")
 sagca = dssFile.get("/AMERICAN/FOLSOM-SAGCA/TOP CON STOR/01JAN2006/1DAY/OBS/")
 inflow = dssFile.get("/AMERICAN/FOLSOM/FLOW-RES IN/01JAN2006/1DAY/OBS/")
 outflow = dssFile.get("/AMERICAN/FOLSOM/FLOW-RES OUT/01JAN2006/1DAY/OBS/")
except java.lang.Exception, e :
 # Take care of any missing data or errors
 MessageBox.showError(e.getMessage(), "Error reading data")
# Add Data
datasets = java.util.Vector()
datasets.add(precip)
datasets.add(stor)
datasets.add(topcon)
datasets.add(sagca)
datasets.add(inflow)
datasets.add(outflow)
# For this code, jython sees a List before a Vector
#list = java.awt.List()
list = []
list.append(datasets)
table = HecDataTableToExcel.newTable()
table.createExcelFile(list, "c:/temp/folsom-export.xlsx")
# If you want to run Excel with a specific name and not a temp name:
#table.runExcel(list "myWorkbook.xls")
# Or, if you would just rather create an Excel file, but not run it:
#table.createExcelFile(datasets, "myWorkbook.xls")