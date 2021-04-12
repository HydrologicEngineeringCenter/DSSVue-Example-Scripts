from hec.heclib.dss import HecDss
import sys

file = R"C:\project\DSSVue-Example-Scripts\data\1PcAEP_360min_5145.dss"
dssfile = HecDss.open(file)

flow = dssfile.get("//Subbasin-1C2/FLOW//1MIN/RUN:1PcAEP_360min_5145/")

file = open(R'c:\temp\output.csv','w')
file.write("Subbasin-1C2\n")
file.write("DateTime,Value\n")
times = flow.getTimes()
i =0
for Q in flow.values:
  t = times.element(i)
  #file.write(str(t.year())+"-"+str(t.month())+"-"+str(t.day())+ " "+str(t.hour())+":"+str(t.minute())+"\n")
  file.write(t.date(-13)+" "+t.time()+","+str(Q)+"\n")
  i=i+1

sys.stdin.readline()
