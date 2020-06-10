from hec.heclib.dss import HecDss

theFile = HecDss.open("MyFile.dss") 
#or 
theFile = HecDss.open("C:/temp/sample.dss", 1) 


#Finished using the file - release it 
theFile.done()