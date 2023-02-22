from hec.heclib.dss import HecDss

fileName= R"C:\project\DSSVue-Example-Scripts\data\examples-all-data-types.dss"

dss = HecDss.open(fileName)
# using flow, (pretending this is stage)
# using read instead of get, so the object returned is based on HecMath
stage=dss.read("/regular-time-series-many-points/unknown/flow/01Sep2004/15Minute//")
table = dss.read("/paired-data/DEER CREEK/STAGE-FLOW///USGS/")
print(type(table))
flow = table.ratingTableInterpolation(stage)
print(flow)

print(flow.getData().values)

