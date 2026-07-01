from hec.io import PairedDataContainer
from hec.model import PairedValuesExt

x_ordinates = [1.0, 2.0, 3.0, 4.0, 5.0]
z_labels = ["10.0", "20.0", "30.0"]

curve_1 = [100.0, 110.0, 120.0, 130.0, 140.0]
curve_2 = [200.0, 220.0, 240.0, 260.0, 280.0]
curve_3 = [300.0, 330.0, 360.0, 390.0, 420.0]

y_ordinates = [curve_1, curve_2, curve_3]

pdc = PairedDataContainer()
pdc.xOrdinates = x_ordinates
pdc.yOrdinates = y_ordinates
pdc.labels = z_labels
pdc.labelsUsed = True
pdc.numberOrdinates = len(x_ordinates)
pdc.numberCurves = len(z_labels)

pve = PairedValuesExt()
pve.setData(pdc)


print(pve.interpolate(2.5, 15.0))
print(pve.interpolate(1.0, 10.1))
print(pve.interpolate(1.0, 10.0))

# output
# 172.5
# 101.0
# 100.0
