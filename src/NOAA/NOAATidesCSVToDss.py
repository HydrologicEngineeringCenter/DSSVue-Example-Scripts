#Description : Downloads CSV for Tides from NOAA and parses to DSS
###############################
import urllib
# import urllib.parse
# import urllib.request
# from urllib.request import urlopen
# import numpy as np
import datetime
import time
import csv
###################################
from hec.script import Plot, MessageBox
from hec.io import TimeSeriesContainer
# from hec.io import PairedDataContainer
# from hec.hecmath import TimeSeriesMath
# from hec.hecmath import PairedDataMath
from hec.heclib.dss import HecDss, DSSPathname
from hec.heclib.util import HecTime
import java
def forecastGoM(begin_date, 
                end_date, 
                station,
                product,
                interval, 
                units, 
                time_zone, 
                datum):
    option={}
    option['begin_date']=begin_date
    option['end_date']=end_date
    option['station']=station
    option['product']=product
    option['interval']=interval
    option['units']=units
    option['time_zone']=time_zone
    option['datum']=datum
    option['application']='web_services'
    option['format']='csv'
    url= 'https://api.tidesandcurrents.noaa.gov/api/prod/datagetter'
    url_values= urllib.urlencode(option)
    full_url= url+'?'+url_values
    print ("Using URL:   ", full_url)
    data=urllib.urlretrieve(full_url)
    #urllib.urlretrieve(full_url, url_values+'.csv') Not sure what this line is doing
    return data

def csvParseToLists(csvFile):
    dList = []
    vList = []
    with open(csvFile) as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            print (row)
            dList.append(row["Date Time"])
            vList.append(row[" Water Level"])    
    return dList, map(float, vList)
                       
def hecTimeParser(timesList):
    hecTimes = []
    for time in timesList:
        try:
            hecTime=HecTime()
            hecTime.set(time)
            hecTimes.append(hecTime.value())
        except Exception, e :
            print e    
    return hecTimes   
         
#########################################################################################
endD = datetime.datetime.utcnow()
endStr = endD.strftime("%Y%m%d %H:00")
startD = endD-(datetime.timedelta(hours=2))
startStr = startD.strftime("%Y%m%d %H:00")

# forecastGoM returns a tuple, first item is the location of the temp file.
csvTempLocation = forecastGoM(startStr,
                               endStr,
                                8764227,
                                "water_level",
                                "",
                                "english",
                                "gmt",
                                "NAVD")[0]
                                                                
dateList, valueList = csvParseToLists(csvTempLocation)
# Trying to trash the temp files when done with them
urllib.urlcleanup()
#convert strings to HecTimes
hecDates = hecTimeParser(dateList)
try :
    myDss = HecDss.open("C:/temp/test.dss", 6)
    tsc = TimeSeriesContainer()
    tsc.fullName = "/Lower Miss/Amerada Pass/STAGE//6MIN/OBS/"
    tsc.interval = 6
    tsc.numberValues= len(valueList)
    tsc.values = valueList
    tsc.times=hecDates
    tsc.units = "FEET"
    tsc.type = "INST-VAL"
    myDss.put(tsc)
    myDss.done()
    print "Done"
except Exception, e :
    print e
except java.lang.Exception, e :
    print e


