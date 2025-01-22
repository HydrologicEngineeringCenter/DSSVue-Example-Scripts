
note: The following was copied from an old HEC web page, it is not tested.

1. Run HEC-DSSVue and open the USGS import function.

2. Select or type in the stations that you want to retrieve.

3. Save the station table, saving only the stations that will be retrieved (from the File menu).

4. Write (edit) a short script that runs the USGS jar (Note: you will not be running HEC-DSSVue):

```jython
  try :
     dssFile = HecDss.open("C:/RtsData/database/Nashville.dss", "T-5D, T")
     usgs = UsgsControlFrame(dssFile)
     usgs.loadStations("C:/RtsData/database/Nashville.usgs")
     istat = usgs.retrieveData()
     dssFile.close()
     
```
     
In this example, we are obtaining the last 5 days of data (“T-5D T”). You can change that time windows to whatever suits your needs, for example, the last 12 hours would be “T-12H, T”.

You will need version 3.x of the USGS jar and version 2.1 or later of HEC-DSSVue. Version 3.3 is included; however, this jar will not work with HEC-DSSVue 2.0 as some class names have changed. Contact Myles McManus (myles.b.mcmanus@usace.army.mil) for a later version.

Here is the complete script. This one runs every 5 minutes, forever.

```jython
   from hec.script import *
   from hec.heclib.dss import *
   from hec.plugins.usgs import *
   import time
   import java
   while (1) :
     try :
       dssFile = HecDss.open("C:/weather/weather.dss", "T-1D, T")
       usgs = UsgsControlFrame(dssFile)
       usgs.loadStations("C:/weather/Stations.usgs")
       usgs.retrieveData()
       dssFile.close()
     except java.lang.Exception, e :
       print "Error: " + e.toString()
     time.sleep(1800)
   # "Done"
```
The script is executed using the Jython.exe include with HEC-DSSVue 2.1 and later. On the PC, it is simply:

   C:\HEC-DSSVue2.1\Jython.exe c:\Weather\runUsgs.py
