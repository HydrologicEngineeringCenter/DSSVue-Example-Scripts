from hecdss import HecDss

dss_file = "FlowData.dss"

dss = HecDss(dss_file)
c = dss.get_catalog()

i=1
for path in c:
    print(f"[{i}] {path}]")
    i+=1
