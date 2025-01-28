# example to convert time-series into paired data following this example:
# https://www.hec.usace.army.mil/confluence/pages/viewpage.action?spaceKey=WG&title=Extracting+Data+from+the+POR+Simulation
#
# pip install -i https://test.pypi.org/simple/ hecdss

# January 2025
# Karl Tarbet and Oskar Hurst

from hecdss import HecDss
from hecdss.paired_data import PairedData
from hecdss.dsspath import DssPath
from hecdss.regular_timeseries import RegularTimeSeries
import calendar

def create_pd(ts:RegularTimeSeries,month:int):
    """ 
    creates a paired data object from a time series, filtered by month
    the paired data (x,y) values are generated as:
     x = zero based index 
     y = the time-series values
     """
    print(len(ts.values))
    subset = [[value] for time, value in zip(ts.times, ts.values) if time.month == month]
    index_array = range(0,len(subset))
    pd = PairedData.create(index_array,subset)
    return pd
    

def convert_ts_to_pd(dss_filename: str, pathname: str):
    """ converts a time-series into paired data by month """
    with HecDss(dss_filename) as dss:
        print(f" record_count = {dss.record_count()}")
        ts = dss.get(pathname)

        for month in range(1, 13):
            print(month)
            pd = create_pd(ts,month)
            p = DssPath(ts.id)
            p.E=""
            p.C="Index-"+p.C
            p.F= p.F+ " "+calendar.month_name[month]
            pd.id = str(p)
            dss.put(pd)

convert_ts_to_pd(r"C:\tmp\POR_Daily.dss","//HHD/ELEVATION//1Day/RUN:POR Daily/")

