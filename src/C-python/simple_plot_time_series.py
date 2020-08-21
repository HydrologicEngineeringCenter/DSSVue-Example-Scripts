import matplotlib.pyplot as plt
import pandas as pd

times = pd.to_datetime(["2001-01-01","2001-01-02",
                "2001-01-03","2001-01-04","2001-01-05",
                "2001-01-01","2001-01-06"],infer_datetime_format=True)
                
df1 = pd.DataFrame({
    'date':times,
    'value':[5,1,0,5,2,2,3]
})
df1.to_csv('simple_csv.csv')
print(df1)
df1.plot(kind='line',x='date',y='value')
plt.show()