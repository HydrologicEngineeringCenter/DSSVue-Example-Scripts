import cwms
from datetime import datetime, timedelta
from hecdss import HecDss
from hecdss.cwms_utility import CwmsUtility
from hecdss import RegularTimeSeries
import hecdss


def read_from_cwms(tsid, office_id, t1, t2):
    print(f'reading, {tsid}')
    data = cwms.get_timeseries(ts_id=tsid, office_id=office_id, begin=begin, end=end)
    return data


def cwms_to_regular_timeseries(data):
    times = data.df['date-time'].to_list()
    values = data.df['value'].to_list()
    cwms_tsid = data.json['name']
    data_type = CwmsUtility.dss_data_type_from_cwms_tsid(cwms_tsid)
    units = data.json['units']
    dss_path = CwmsUtility.cwms_ts_id_to_dss_path(cwms_tsid)

    if dss_path.E[:2].lower() == "ir":
        raise ValueError(f"Irregular time series not implemented in cwms_to_timeseries method input: {cwms_tsid}")

    ts = RegularTimeSeries.create(values, times, units=units, dataType=str(data_type), interval=dss_path.E,
                                  path=str(dss_path))
    ts.id = str(dss_path)
    return ts


def regular_time_series_to_json(rts: RegularTimeSeries, office_id: str, ts_id: str):
    """
    converts a regular timeseries into a JSON format that is
    compatible with the CWMS data API
    """
    # hard coding flag = 0
    flag = 0  # TO DO, make optional, only if DSS data has quality column
    # dss quality code is the same cwms
    values = [[d, v, flag] for d, v in zip(rts.times, rts.values)]

    # df = pd.DataFrame(values, columns = ['date-time', 'value','quality-code'])
    #
    # rts.create_df()  # future method?

    json_result = {'name': ts_id,
                   'office-id': office_id,
                   'units': rts.units,
                   'values': values,
                   # 'values': [['2024-04-23T08:15:00-06:00', 86.57, 3],
                   #            ['2024-04-23T08:30:00', 86.57, 3],
                   #            ['2024-04-23T08:45:00', 86.57999999999997, 3],
                   #            ['2024-04-23T09:00:00', 86.57999999999997, 3],
                   #            ['2024-04-23T09:15:00', 86.57999999999997, 3],
                   #            ['2024-04-23T09:30:00', 86.57999999999997, 3],
                   #            ['2024-04-23T09:45:00', 86.59, 3],
                   #            ['2024-04-23T10:00:00', 86.57999999999997, 3]],
                   'version-date': None}

    return json_result


if __name__ == '__main__':
    end = datetime.now()
    begin = end - timedelta(days=5)
    office_id = "SWT"
    ts_id = 'TULA.Flow.Inst.1Hour.0.Ccp-Rev'
    data = read_from_cwms(ts_id, office_id, begin, end)
    ts = cwms_to_regular_timeseries(data)
    dss = HecDss(r"c:\temp\myfile.dss")
    dss.put(ts)
    dss_ts = dss.get(ts.id)
    json = regular_time_series_to_json(dss_ts, office_id, ts_id)
    print(json)
    # save to CDA with version-"copy"
    # cwbi-test
    # write to CDA with url = cwbi-test
    # set key

# Karl's help wanted questions
# could the list of list of [[date, value],[date, value]]  be a list of tuple ?  list (date,value), (date,value)

# what about nan  (is that OK?)
# 'values': [[datetime.datetime(2024, 8, 23, 1, 0), nan, 0],
