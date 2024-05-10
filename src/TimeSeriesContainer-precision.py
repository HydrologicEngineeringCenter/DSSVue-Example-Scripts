from hec.heclib.dss import HecDss
from hec.heclib.util import HecDouble

# read time series, print tsc.precision
# print a number

path = "/OKEECHOBEE/S270/ELEV-HEAD//15MIN//"
file = r"C:\project\doc\mobile-web\drs.dss"
dss = HecDss.open(file)
tsc = dss.get(path)
tsc.precision = 2
dss.put(tsc)
tsc = dss.get(path)

print("precision = "+str(tsc.precision))
print("raw value = "+str(tsc.values[0]))
value = HecDouble()
value.set(tsc.values[0])
value.setPrecision(tsc.precision)
print("with precision="+str(tsc.precision)+" output value = "+str(value.toString()))
#tsc.precision=2
#value.setPrecision(tsc.precision)
#print("with precision="+str(tsc.precision)+" value = "+str(value.toString()))
