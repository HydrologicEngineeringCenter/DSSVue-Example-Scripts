import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from hecdss import HecDss


# pip install -i https://test.pypi.org/simple/ hecdss
# pip install matplotlib


dss_file = "FlowData.dss"
pathname = "/CUMBERLAND RIVER/BARBOURVILLE/FLOW//30Minute/OBS/"
with HecDss(dss_file) as dss:

    catalog = dss.get_catalog()
    for p in catalog:
        print(p)

    ts = dss.get(pathname)

    values = ts.values
missing_value = -340282346638528859811704183484516925440.000000
indices = np.where(np.isclose(values, missing_value, rtol=0, atol=0, equal_nan=True))[0]
values[indices] = None

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

