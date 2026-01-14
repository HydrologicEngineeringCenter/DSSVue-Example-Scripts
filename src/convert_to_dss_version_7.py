from hec.heclib.dss import HecDss
from hec.heclib.dss import HecDSSUtilities
from hec.heclib.util import Heclib
import os


def delete_file(filename):
  if os.path.exists(filename):
    try:
        os.remove(filename)
    except OSError as e:
        print "Error: deleting  file "+filename

def convert_to_dss_version_7(filename):
  """ 
  converts filename to a version 7 DSS file if necessary.
  """
  if Heclib.zgetFileVersion(filename) == 7:
    print("already  a version 7 file")
    return
  base_name, extension = os.path.splitext(filename)
  tmp_filename = base_name + "_backup"+  extension
  delete_file(tmp_filename)
  os.rename(filename, tmp_filename)
  h = HecDSSUtilities()
  h.setDSSFileName(tmp_filename)
  h.convertVersion(filename)
  h.close()


filename= r"c:\tmp\forecast.dss"
delete_file(filename)
dss6 = HecDss.open(filename,6)  # force a dss 6 file for testing only works with older software.
dss6.close()

convert_to_dss_version_7(filename)
convert_to_dss_version_7(filename)  # try again, but already version 7 

print("done")
