# Reads a cross section text file and saves to DSS paired-data records
#
# Example usage using HEC-DSSVue.exe from the command line:
# c:\>C:\bin\HEC-DSSVue-3.4.15\HEC-DSSVue.exe C:\project\DSSVue-Example-Scripts\src\PariredData\cross-section-to-paired-data.py
#
# The script can also be run from the DSSVue Script Editor (Tools-Script Editor)

from hec.script import HecDss
from hec.io import PairedDataContainer
from java.lang import Double
from java.lang.reflect import Array

inputFile = r"C:\project\DSSVue-Example-Scripts\src\PariredData\xs_points2.txt"   # tab-delimited input
dssFile   = r"C:\project\DSSVue-Example-Scripts\src\PariredData\xs_points2.dss"  # output DSS file


def read_reaches(path):
    # xs will map reach_id -> [ list_of_distances, list_of_elevations ]
    xs = {}
    with open(path, 'r') as f:
        # skip header
        header = f.readline()
        for line in f:
            line = line.strip()
            if not line:
                continue
            # split on tabs (or whitespace)
            parts = line.split('\t')
            if len(parts) < 3:
                continue
            reach_id, dist_s, elev_s = parts[0], parts[1], parts[2]
            # parse numbers
            try:
                dist  = float(dist_s)
                elev  = float(elev_s)
            except ValueError:
                # skip bad lines
                continue
            # initialize lists if first time we see this reach_id
            if reach_id not in xs:
                xs[reach_id] = [[], []]
            # append to distance list and elevation list
            xs[reach_id][0].append(dist)
            xs[reach_id][1].append(elev)
    return xs


def convert_to_java(jython_1d_list):
    cols = len(jython_1d_list)
    java_2d_array = Array.newInstance(Double.TYPE, 1, cols)

    for j in range(cols):
        java_2d_array[0][j] = float(jython_1d_list[j])

    return java_2d_array

# read cross section data
cross_sections = read_reaches(inputFile)

dss = HecDss.open(dssFile)

for reachId, (distances, elevations) in cross_sections.items():
  print(reachId)
  pdc = PairedDataContainer()
  pdc.xOrdinates = distances
  #print(elevations)
  pdc.yOrdinates = convert_to_java(elevations)
  #print(pdc.yOrdinates)
  pdc.numberCurves    = 1
  pdc.numberOrdinates = len(elevations)
  pdc.setFullName( "//{0}/DISTANCE-ELEVATION///TABLE/".format(reachId));
 
  dss.put(pdc)

print("done.")
 
