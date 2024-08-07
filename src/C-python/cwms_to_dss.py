import cwms
from datetime import datetime, timedelta
from hecdss import HecDss
from hecdss.regular_timeseries import RegularTimeSeries

def read_from_cwms(tsid, office_id, t1, t2):
    print(f'reading, {tsid}')
    data = cwms.get_timeseries(tsId=tsid, office_id=office_id, begin=begin, end=end)
    return data

def write_to_dss(ts,path):
    dss = HecDss("myfile.dss")
    ts.id = path
    dss.put(ts)

def dss_data_type_from_cwms_tsid(cwms_tsid):
    """
    takes an input id such as 'TULA.Flow.Inst.1Hour.0.Ccp-Rev'
    and returns the DSS DataType  'INST-VAL' in this example
    :param cwms_tsid: input time-series identifier
    :return:
    """
    parts = cwms_tsid.split('.')
    ts_type = parts[2]
    if ts_type.lower() == "inst":
        result = "INST-VAL"
    elif ts_type.lower() == "total":
        result = "PER-CUM"
    elif ts_type.lower() == "ave":
        result = "PER-AVER"
    elif ts_type.lower() == "max":
        result = "PER-MAX"
    elif ts_type.lower() == "min":
        result = "PER-MIN"
    else:
        result = ts_type
    return result

def get_dss_interval(cwms_tsid):
    """
     takes an input id such as 'TULA.Flow.Inst.1Hour.0.Ccp-Rev'
    and returns the DSS interval  '1Hour' in this example
    :param cwms_tsid:
    :return:
    """
    return cwms_tsid.split('.')[3]
def cwms_to_timeseries(data):
    timestamps = data.df['date-time'].to_list()
    times = [ datetime.fromisoformat(str(dt)) for dt in timestamps]
    values = data.df['value'].to_list()
    cwms_tsid = data.json['name']
    data_type = dss_data_type_from_cwms_tsid(cwms_tsid)
    units = data.json['units']
    interval = get_dss_interval(cwms_tsid)
    if interval[:2].lower() == "ir":
        raise ValueError(f"Irregular time series not implemented in cwms_to_timeseries method input: {cwms_tsid}")

    ts = RegularTimeSeries.create(values,times,units=units,dataType = data_type)
    return ts


if __name__ == '__main__':
  end = datetime.now()
  begin = end - timedelta(days=5)
  data = read_from_cwms('TULA.Flow.Inst.1Hour.0.Ccp-Rev','SWT', begin,end)

  ts = cwms_to_timeseries(data)
  write_to_dss(ts,"/TULA//Flow//1Hour/Ccp-Rev/")
