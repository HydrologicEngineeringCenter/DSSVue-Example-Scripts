from hec.heclib.dss import HecDss # for DSS
from hec.script import Tabulate,TableExportOptions # for Tabulate
file = r"C:\project\DSSVue-Example-Scripts\data\sample.dss" # specify the DSS file
dssfile = HecDss.open(file) # open the file

#read 2 records

stage = dssfile.get("/MY BASIN/RIVERSIDE/STAGE//1HOUR/OBS/")
flow = dssfile.get("/RUSSIAN/NR HOPLAND/FLOW//1HOUR//")
theTable = Tabulate.newTable() # create the table
theTable.setTitle("Test Table") # set the table title
theTable.setLocation(5000,5000) # set the location of the table off
#                                the screen
theTable.addData(flow) # add the data
theTable.addData(stage)
theTable.showTable() # show the table
flowCol = theTable.getColumn(flow) # adjust columns
stageCol = theTable.getColumn(stage)

flowWidth = theTable.getColumnWidth(flowCol)
stageWidth = theTable.getColumnWidth(stageCol)
theTable.setColumnPrecision(flowCol, 0)
theTable.setColumnPrecision(stageCol, 2)
theTable.setColumnWidth(flowCol, flowWidth - 10)
theTable.setColumnWidth(stageCol, stageWidth + 10)
opts = TableExportOptions()# get new export options
opts.delimiter = ","# delimit with commas
opts.title = "My Table"# set the title
fileName = "c:/temp/table.txt"# set the output file name
theTable.stayOpen()
theTable.export(fileName, opts)# export to the file
theTable.close()# close