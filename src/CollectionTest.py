from hec.script import Plot
from hec.io import TimeSeriesCollectionContainer
from hec.heclib.dss import HecDss, DSSPathname,HecTimeSeries

#import java
# this first script verifies whether a pathname is a collection or member of a collection
iscollection = DSSPathname. isaCollectionPath("//CP3/FLOW/01FEB2018/1HOUR/C:000008|--A0S0/")
T=R"//CP3/FLOW/01FEB2018/1HOUR/C:000008|--A0S0/"
print iscollection

# this script takes a pathname and sets a sequence ID in the pathame
PP=DSSPathname("/CORALITOS CREEK/FREEDOM/FLOW/01JAN1956/1DAY/GMT/")
# DSSPathname. setCollectionSequence(String collectionSequence) 
PP.setCollectionSequence(5)
print PP

# this script creates a timeseries collection container, retrieves the collection prints true and prints size of the collection
# DSSPathname. setCollectionSequence(int collectionSequence) 
#java: HecTimeSeries timeSeries = new HecTimeSeries();
timeSeries = HecTimeSeries()
tscc = TimeSeriesCollectionContainer()
# fullName is method in HecTimeSeries
tscc.fullName =T
tscc.fileName = R"C:\Temp\CWMS 3.2.2 14 May 2021\forecast\Demo-2018-02-08\Ensemble_Example_Watershed\forecast.dss"
timeSeries.setRetrieveAllTimes(True)
istatus = timeSeries.read(tscc, True)
print istatus
# add close parentheses after method
print tscc.size()
