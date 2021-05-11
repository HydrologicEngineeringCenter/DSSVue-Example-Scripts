#Description : Downloads CSV for Tides from NOAA and parses to DSS
#Instructions : This script can be used from the command line using 
#               the parser options described below.
#    <command> <filename> <options>
# ie: "jython NOAATidesCSVToDSS.py -g amerada -n 8764227"
# copy and paste the line above (without quotes) into the command line while 
# within the directory containing the NOAATidesCSVToDss.py script.
#
# The only option that does not have a default is gage_number or -n
# This must be provided.
#
###############################
import urllib
# import urllib.parse
# import urllib.request
# from urllib.request import urlopen
# import numpy as np
import datetime
import time
import csv
from optparse import OptionParser
###################################
from hec.script import Plot, MessageBox
from hec.io import TimeSeriesContainer
# from hec.io import PairedDataContainer
# from hec.hecmath import TimeSeriesMath
# from hec.hecmath import PairedDataMath
from hec.heclib.dss import HecDss, DSSPathname
from hec.heclib.util import HecTime
import java

parser = OptionParser()

###NOAA options
parser.add_option("-n", "--gage_number", action="store", type="int", dest="gage_number")
parser.add_option("-g", "--gage_name", action="store", type="string", dest="gage_name", default="gage")
parser.add_option("-p", "--product", action="store", type="string", dest="product", default="water_level")
parser.add_option("-i", "--interval", action="store", type="string", dest="interval", default="60")
parser.add_option("-u", "--units", action="store", type="string", dest="units", default="english")
parser.add_option("-t", "--timezone", action="store", type="string", dest="timezone", default="gmt")
parser.add_option("-d", "--datum", action="store", type="string", dest="datum", default="NAVD")

###Timeseries container options
parser.add_option("-N", "--tscn", action="store", type="string", dest="tsc_fullName", default="")
parser.add_option("-U", "--tscu", action="store", type="string", dest="tsc_units", default="FEET")
parser.add_option("-T", "--tsct", action="store", type="string", dest="tsc_type", default="INST-VAL")

(options, args) = parser.parse_args()

def NOAA_gage_data_request(begin_date, 
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
csvTempLocation = NOAA_gage_data_request(startStr,
                               endStr,
                                options.gage_number,
                                options.product,
                                options.interval,
                                options.units,
                                options.timezone,
                                options.datum)[0]
                                                                
dateList, valueList = csvParseToLists(csvTempLocation)
# Trying to trash the temp files when done with them
urllib.urlcleanup()
#convert strings to HecTimes
hecDates = hecTimeParser(dateList)
try :
    myDss = HecDss.open(options.gage_name+".dss", 6)
    tsc = TimeSeriesContainer()
    tsc.fullName = options.tsc_fullName
    tsc.numberValues= len(valueList)
    tsc.values = valueList
    tsc.times=hecDates
    tsc.units =  options.tsc_units
    tsc.type =  options.tsc_type
    myDss.put(tsc)
    myDss.done()
    print "Done"
except Exception, e :
    print e
except java.lang.Exception, e :
    print e


