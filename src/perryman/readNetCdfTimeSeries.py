import os, sys
sys.path.append("./netcdfAll-5.5.3.jar")
from hec.heclib.dss              import HecDss
from hec.heclib.util             import HecTime
from hec.heclib.util             import Heclib
from hec.io                      import TimeSeriesContainer
from mil.army.usace.hec.metadata import IntervalFactory
from ucar.nc2                    import NetcdfFiles

#-------------------#
# get the filenames #
#-------------------#
if len(sys.argv) == 1 :
	print("No NetCDF filename specified")
	exit(1)
netcdf_filename = sys.argv[1]
if len(sys.argv) > 2 :
	dss_filename = sys.argv[2]
else :
	dss_filename = os.path.splitext(netcdf_filename)[0] + ".dss"

#-------------------------------------------------------------------------------#
# get the minutes offset between minutes in netcdf file and minutes in dss file #
#-------------------------------------------------------------------------------#
hec_time = HecTime()
hec_time.set("01Jan1970, 0000") 
hec_time_minutes_offset = hec_time.value()

dimensions = {
	"stations"       : 0, 
	"time"           : 0, 
	"realization"    : 0,
	"char_leng_id"   : 0,
	"char_leng_name" : 0
}

variables = {
	"station_id"    : None,
	"station_names" : None,
	"time"          : None,
	"analysis_time" : None,
	"x"             : None,
	"y"             : None,
	"z"             : None,
	"SQME"          : None,
}

stations = []

ncf = None
ncf = NetcdfFiles.open(netcdf_filename)
if ncf :
	try :
		Heclib.zset("MLVL", "", 0)
		dss = HecDss.open(dss_filename)
		print("Opened NetCDF file: %s" % netcdf_filename)
		print("Opened DSS file:    %s" % dss_filename)
		#--------------------#
		# get the dimensions #
		#--------------------#
		for dim in dimensions :
			try    : dimensions[dim] = ncf.findDimension(dim).getLength()
			except : raise Excepttion("Couldn't find expected dimension: %s" % dim)
		print("\nNumber of realizations = %d" % dimensions["realization"])
		#-------------------#
		# get the variables #
		#-------------------#
		for var in variables :
			variables[var] = ncf.findVariable(var)
			if variables[var] is None : raise Exception("Couldn't find expected variable: %s" % var)
		for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789" :
			var = "QIIC%c" % c
			v = ncf.findVariable(var)
			if v is not None :
				variables[var] = v
		#-----------------------#
		# get the analysis time #
		#-----------------------#
		analysis_time = int(variables["analysis_time"].readScalarDouble())
		hec_time.set(analysis_time+hec_time_minutes_offset)
		print("\nAnalysis time = %s" % hec_time.dateAndTime(4))
		#----------------------#
		# get the station info #
		#----------------------#
		x = variables["x"].read()
		y = variables["y"].read()
		z = variables["z"].read()
		print("\nStations:")
		max_station_id_len = 0
		for s in range(dimensions["stations"]) :
			stations.append({})
			ary = variables["station_id"].read("%d,0:%d" % (s, dimensions["char_leng_id"]-1))
			station_id = ""
			for c in range(dimensions["char_leng_id"]) : station_id += ary.getChar(c)
			station_id = station_id.strip(" \t\0")
			max_station_id_len = max(max_station_id_len, len(station_id))
			ary = variables["station_names"].read("%d,0:%d" % (s, dimensions["char_leng_name"]-1))
			station_name = ""
			for c in range(dimensions["char_leng_name"]) : station_name += ary.getChar(c)
			stations[s]["id"] = station_id
			stations[s]["name"] = station_name.strip(" \t\0")
		for s in range(dimensions["stations"]) :
			print('\t%s  %f,%f,%f  "%s"' % (stations[s]["id"].ljust(max_station_id_len), x.getDouble(s), y.getDouble(s), z.getDouble(s), stations[s]["name"]))
		#---------------------------------------------#
		# get the data times and compute the interval #
		#---------------------------------------------#
		times = variables["time"].read()
		hec_times = []
		for t in range(dimensions["time"]) :
			hec_times.append(int(times.getDouble(t))+hec_time_minutes_offset)
			hec_time.set(hec_times[t])
		end_time_str = hec_time.dateAndTime(4)
		interval = hec_times[1] - hec_times[0]
		for t in range(2, len(hec_times)) :
			if hec_times[t] - hec_times[t-1] != interval :
				raise Exception("Irregular interval data in file!")
		hec_time.set(hec_times[0])
		interval_name = IntervalFactory.findAnyDss(IntervalFactory.equalsMinutes(interval)).get().getInterval()
		print("\nTimes: %s - %s, interval = %s (%d values)" % (hec_time.dateAndTime(4), end_time_str, interval_name, dimensions["time"]))
		#----------------------------#
		# get the time series values #
		#----------------------------#
		for v in [v for v in variables if v == "SQME" or v.startswith("QIIC")] :
			unit = variables[v].findAttribute("units").getStringValue()
			ensemble = variables[v].findAttribute("ensemble").getStringValue()
			missing = variables[v].findAttribute("_FillValue").getNumericValue()
			print("\nProcessing variable %s, unit = %s" % (v, unit))
			for s in range(dimensions["stations"]) :
				sys.stdout.write("\tStation %s  " % stations[s]["id"].ljust(max_station_id_len))
				for r in range(dimensions["realization"]) :
					tsc = TimeSeriesContainer()
					tsc.location = stations[s]["id"]
					tsc.parameter, tsc.subParameter = "Flow", v
					tsc.interval = interval
					tsc.type = "PER-AVER" if v == "SQME" else "INST"
					tsc.units = unit
					tsc.fullName = "//%s/%s-%s//%s/C:%6.6d|%s/" % (tsc.location, tsc.parameter, tsc.subParameter, interval_name, r, ensemble)
					tsc.numberValues = dimensions["time"]
					tsc.times = hec_times[:]
					sys.stdout.write(".")
					ary = variables[v].read("0:%d,%d,%d" % (len(hec_times)-1, r, s))
					values = []
					for t in range(dimensions["time"]) :
						value = ary.getFloat(t)
						values.append(Heclib.UNDEFINED_DOUBLE if value == missing else value)
					tsc.values = values
					dss.put(tsc)
				print("")
	finally :
		ncf.close()
		print("\nClosed NetCDF file: %s" % netcdf_filename)
		dss.close()
		print("Closed DSS file:    %s" % dss_filename)
