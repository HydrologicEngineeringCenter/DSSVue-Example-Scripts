import matplotlib.pyplot as plt
import pandas as pd
from pydsstools.heclib.dss import HecDss
from pydsstools.heclib.dss.HecDss import Open

dss_file = "FlowData.dss"
pathname = "/CUMBERLAND RIVER/BARBOURVILLE/FLOW//30MIN/OBS/"
pathname2 = "/CUMBERLAND RIVER/CUMBERLAND FALLS/FLOW//30MIN/MISSING/"
pathname3 = "/CUMBERLAND RIVER/CUMBERLAND FALLS/FLOW//30MIN/OBS/"
pathname4 = "/CUMBERLAND RIVER/WILLIAMSBURG/FLOW//30MIN/OBS/"

fid = HecDss.Open(dss_file)
pathArr = [pathname,pathname2, pathname3, pathname4]
names = ["data1", "data2", "data3","data4"]

ts = fid.read_ts(pathname)
values = ts.values

pd.to_datetime(["2001-01-01","2001-01-02",
                "2001-01-03","2001-01-04","2001-01-05",
                "2001-01-01","2001-01-06"]
                
['2/25/10', '8/6/17', '12/15/12'], format='%m/%d/%y')

df1 = pd.DataFrame({
    'date':times,
    'value':[5,1,0,5,2,2,3]
})
print(df1)
df1.plot(kind='line',x='date',y='value')
plt.show()
exit(-1)

df = pd.DataFrame(ts.pytimes, columns=['Dates'])
i = 0

for path in pathArr:
    ts = fid.read_ts(path)
    df[names[i]] = ts.values
    i += 1

#df.drop(['Dates'],axis = 1).plot(subplots = True)
df.plot(subplots = True)
plt.show()
print(df)

# dataSet = {'Dates': ts.pytimes, 'Data': ts.values}
# df = pd.DataFrame(dataSet)
# df.plot(x='Dates', y='Data', kind='line')
# plt.show()

# for info in values:
#     dates.append(str(ts.pytimes[i]))
#     data.append(info)
#     # print(str(ts.pytimes[i]) + "," + str(data))
#     # print(str(ts.pytimes[i]))
#     i += 1


# plt.plot(times[~ts.nodata],values[~ts.nodata],"o")
# plt.show()
# fid.close()
