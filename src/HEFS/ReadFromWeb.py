from urllib2 import urlopen
from zipfile import ZipFile
import csv

def readCSV(fileName):
  data=list(csv.reader(open(fileName)))
  return data

def downloadFile(url,destinationFileName):
  r = urlopen(url)
  data = r.read()
  with open(destinationFileName,'wb') as f:
    f.write(data)

def unzipFiles(zipFileName,destDir):
  z = ZipFile(zipFileName)
  #firstOne = z.namelist()[0]
  #print("firstOne:"+firstOne)
  #ZipFile.extract(member, path=None, pwd=None)
  #z.extrac(firstOne,dest)
  z.extractall(destDir)

forecastDate="2019092312" # year MM dd hh
watershedName="RussianNapa"
fileName = forecastDate+"_"+ watershedName + "_hefs_csv_hourly"


#url = "https://www.cnrfc.noaa.gov/csv/2019092312_RussianNapa_hefs_csv_hourly.zip"
_rootUrl = "https://www.cnrfc.noaa.gov/csv/"
webrequest = _rootUrl+ fileName + ".zip"

# downloadFile(webrequest,"c:/temp/"+fileName+".zip")
# unzipFiles("c:/temp/"+fileName+".zip","c:/temp/")
data = readCSV("c:/temp/"+fileName+".csv")
print(data[0])  
print(data[1])  
print(data[2])  

#['2019-10-22 03:00:00', '0.01172', '0.01152', '0.01073 ...
#['2019-10-22 04:00:00', '0.01172', '0.01152', '0.01073 ...


sys.stdin.readline()
