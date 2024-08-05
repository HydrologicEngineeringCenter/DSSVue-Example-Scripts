import matplotlib.pyplot as plt
import pandas as pd
from hecdss import HecDss

dss_file = "FlowData.dss"
pathname = "/CUMBERLAND RIVER/BARBOURVILLE/FLOW//30Minute/OBS/"
dss = HecDss(dss_file)

catalog = dss.get_catalog()
for p in catalog:
    print(p)

ts = dss.get(pathname)

values = ts.values
MISSING =-3.4028234663852886e+38
tolerance = 100000
values = [ None if abs(x - MISSING) < tolerance else x for x in values]
df1 = pd.DataFrame({
    'date':ts.times,
    'value':values
})
# save to CSV
df1.to_csv("BARBOURVILLE.csv")

print(df1)
# plot
df1.plot(kind='line',x='date',y='value')
plt.show()
exit(-1)

