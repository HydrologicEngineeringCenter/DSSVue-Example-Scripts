from hec.heclib.dss import HecDss, DSSPathname
import sys

file = R"C:\project\DSSConversions\HEFS_To_DSS\bin\Debug\hefs_to_dss\test1.dss"
dssfile = HecDss.open(file)
path ="/RussianNapa/APCC1/Flow/01Apr2021/1Hour/C:000005|T:1122021/"
print (DSSPathname.isaCollectionPath(path))



sys.stdin.readline()
