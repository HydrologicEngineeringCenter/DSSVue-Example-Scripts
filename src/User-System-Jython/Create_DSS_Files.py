import sys
sys.path.append(r"C:\local_software\HEC-DSSVue-v4.0.00.345\jar\sys\jythonUtils.jar")
sys.path.append(r"C:\local_software\HEC-DSSVue-v4.0.00.345\jar\hec.jar")
sys.path.append(r"C:\local_software\HEC-DSSVue-v4.0.00.345\jar\jython-standalone-2.7.0.jar")
sys.path.append(r"C:\local_software\HEC-DSSVue-v4.0.00.345\jar\hec-dssvue-dev.jar")
sys.path.append(r"C:\local_software\HEC-DSSVue-v4.0.00.345\jar\rma.jar")

try:
    from hec.heclib.dss import HecDss
    from hec.io import TimeSeriesContainer
    print 'Sucessfully found DSS API'
except:
    print 'import from DSS failed'

fid = HecDss.open(r'C:\workspace\git_clones\vortex_scripting\test_dss_create.dss')
fid.close()


fid = HecDss.open(r'C:\workspace\git_clones\vortex_scripting\test_dss_create_v6.dss',6)
fid.close()
