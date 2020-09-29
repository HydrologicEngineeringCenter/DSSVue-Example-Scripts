# compress/squeeze a dss file
import sys
from hec.heclib.util import Heclib

filename=sys.argv[1] + "\\sample.dss"

Heclib.Hec_squeezeDSS(filename)
print "file was squeezed"



 
