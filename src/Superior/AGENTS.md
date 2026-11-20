
## Summary

We are writing a Jython program to read csv files and store the time series data into a DSS file. 

First Version will just print structure to the screen without any DSS, so it should be designed keeping DSS separate from the CSV parsing.

There are some examples here:  C:\project\DSSVue-Example-Scripts\src  (but please ignore the C-python dir that's for regular python)


##  Details on the CSV File format.

The file begins with a header such as:

```
Daily data for a single subbasin.
Lake:    ,sup
Subbasin:,1
Area:    ,  0.97070E+10
Starts(YMD):,1940-01-01
Ends(YMD):  ,2025-07-23
NewDataStart(YMD):,2025-07-24
Date      ,AirTempMin,AirTempMax,    Precip,   AirTemp,  Dewpoint, Windspeed,CloudCover
YYYY-MM-DD,   Celsius,   Celsius,Millimeter,   Celsius,   Celsius,Meters/Sec,   Percent
```

The YYYY-MM-DD is the signal for end of header.

## Goal

Create a file subbasin_to_dss.py 

The program should be kept simple; don't overdesign.  The CSV is well formed, Fortran output , so a simple split on commas can be used to parse.   I suggest a simple method to read the file that returns all the data in a sturcture such as this example , but parsing actual values from the csv files.

```
contents {
    header {
      title: 'Daily data for a single subbasin.',
      Lake: 'sup',
      Area:  0.97070E+10,
      start: '1940-01-01',
      end:  '2025-07-23',
      column_names : ['AirTempMin','AirTempMax','Precip','AirTemp','Dewpoint','Windspeed','CloudCover'],
      units: ['Celsius','Celsius','Millimeter','Celsius', 'Celsius','Meters/Sec','Percent']
   }
   time_series_times : []
   time_series_values : [[]]  # 
}
```

Will run with:

C:\bin\HEC-DSSVue-4.2.3\jython.exe subbasin_to_dss.py  output.dss <input_dir>

Where:
   <input_dir> is directory to find csv files.
   output.dss is the ouput from the program.

The output DSS file will contain dss data sets for each column of data in the csv file.  The Date Column is first an is referenced for all other columns.

Each Time-series will have a DSS path name   /a/b/c/d/e/f/

Where:
```
a : 'Superior'  # hard-coded
b : get from header["Lake"] + " " + header["Subbasin"]
c : column_names[i] 
d : <leave blank>
e : 1Day
f : 'GLSHFS-OPERATIONAL-HISTORIC' 
```

When writing to DSS the units on the TimeSeriesContainer