from hec.heclib.util import HecTime
from java.util import SimpleTimeZone

t = HecTime("17Jul2024 15:00")
eastern = TimeZone.getTimeZone("America/New_York");
gmt = TimeZone.getTimeZone("GMT");

print(t)
print("converting...")
HecTime.convertTimeZone(t,gmt,eastern)
print(t)
