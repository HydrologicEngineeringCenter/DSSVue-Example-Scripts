# works on HEC software using hec-monolith-3.1.11
# Should work on later versions
# hec.heclib.util.HecTime.getLocalDateTime added circa Aug 2021

import datetime
from hec.heclib.util import HecTime

def convertHecTimeToDatetime(hecTime):
    date = datetime.datetime.strptime(hecTime.getLocalDateTime().toString(), format ="%Y-%m-%dT%H:%M")
    return date

hecTime = HecTime("21Jan2023 2400")
pythonTime = convertHecTimeToDatetime(hecTime)