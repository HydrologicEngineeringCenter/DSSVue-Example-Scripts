# compress/squeeze a dss file
import sys
from hec.heclib.util import Heclib

filename="c:/temp/sample.dss"
if len(sys.argv) != 2:
  filename=sys.argv[1]
#  print("Usage: Compress.py file.dss")
#  exit(-1)

Heclib.Hec_squeezeDSS(filename)
print "file was squeezed"



 
