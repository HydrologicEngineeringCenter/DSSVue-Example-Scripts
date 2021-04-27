from hec.heclib.util import Heclib

fn6="c:/temp/cdec6.dss"
fn7="c:/temp/cdec7.dss"

status = Heclib.zconvertVersion(fn6, fn7)
# convert back to DSS 6

fn6="c:/temp/back-to-cdec6.dss"
status = Heclib.zconvertVersion(fn7, fn6)

