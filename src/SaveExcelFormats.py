from hec.script import MessageBox
from hec.heclib.dss import HecDss
from hec.dataTable import HecDataTableToExcel
import java
import sys
import os
# Open the file and get the data
fileName= R"C:\project\DSSVue-Example-Scripts\data\sample.dss"
xlsFileName = R"c:\tmp\inflow.xls"

dssFile = HecDss.open(fileName, "10MAR2006 2400, 09APR2006 2400")
inflow = dssFile.get("/AMERICAN/FOLSOM/FLOW-RES IN/01JAN2006/1DAY/OBS/")


datasets = java.util.Vector()
datasets.add(inflow)

# For this code, jython sees a List before a Vector
#list = java.awt.List()
list = []
list.append(datasets)
table = HecDataTableToExcel.newTable()
# If you want to run Excel with a specific name and not a temp name:
table.createExcelFile(list, xlsFileName)
# Or, if you would just rather create an Excel file, but not run it:
#table.createExcelFile(datasets, "myWorkbook.xls")
