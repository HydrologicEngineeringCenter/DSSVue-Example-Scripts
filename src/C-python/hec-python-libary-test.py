from hec import DssDataStore

dss = DssDataStore.open(r"C:\project\dss-file-collection\Arroyo_Seco_Streamflow_Old\.dss")

catalog = dss.catalog()
 for p in catalog:
    print(p)
   
ts = dss.retrieve("/ARROYO SECO/PASADENA CA/FLOW/01Oct1988-01Aug2022/15Minute/GMT/\")
print(ts.values[:100])
estimated_ts = ts.estimate_missing_values(543)
print(ts.number_missing_values)
print(estimated_ts.number_missing_values)
dss.is_read_only=False
estimated_ts.version="GMT-estimated missing"
print(estimated_ts)
dss.store(estimated_ts)
dss.close()
