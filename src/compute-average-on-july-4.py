from hec.heclib.util import HecTime

from hec.heclib.dss import HecDss, DSSPathname

def isTargetDate(t):
  return t.month()==7 and  t.day()==4

print ("hi2")

dss = HecDss.open("C:\project\DSSVue-CWMSVue\Hickey-DssVue30minDemo\Data for EFM relationships.dss")
flow = dss.get("/SAN JOAQUIN/VERNALIS/FLOW//1Day/GAGED/")
print flow.units
times = flow.getTimes()
i = 0
count =0
avg =0
for Q in flow.values:
  t = times.element(i)
  if isTargetDate(t) :
    avg += Q
    count+=1
  i = i+1

avg = avg/count
print "Average: "+str(avg)

print "done"
