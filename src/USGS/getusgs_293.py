#!/bin/env jython
'''
Usage

  The getUsgs program is a Jython script which can be executed in any 
  environment in which hec.jar and heclib.jar are available on the classpath. 
  In order to store data to a CWMS Oracle database, dbiClient.jar and 
  cwmsdb.jar are also required.

  The program includes a "shebang" for automatic interpreter loading on UNIX-
  like environments, allowing execution using the "getUSGS" command. On 
  Windows the program can be executed using the command "jython getUSGS", which
  also works on UNIX-like environments. In the examples below, "getUSGS" is 
  used for simplicity.

Command Line

  Program execution via the command line has the form "getUSGS options", where
  options is comprised of the following:

  * -l locations_filename (or --locations locations_filename) - specifies 
       locations input file. Defaults to Locations.csv in the working directory.

  * -p parameters_filename (or --parameters parameters_filename) - specifies 
       parameters  input file. Defaults to Parameters.csv in the working
       directory.

  * -a parameter_aliases_filename (or --aliases parameter_aliases_filename) - 
       specifies parameter aliases input file. Defaults to Parameter_Aliases.csv
       in the working directory.

  * -u (or --usgs) - specifies outputting data as USGS RDB format text.

  * -s (or --shef) - specifies outputting data as SHEF format text.

  * --tzshef shef_time_zone - specifies time zone to use for SHEF messages. If
       not specified, the SHEF messages will be in the time zone specified in
       the USGS text.
       Valid values for shef_time_zone_are:
         + GMT
         + UTC
         + Z  
         + EST
         + EDT
         + CST
         + CDT
         + MST
         + MDT
         + PST
         + PDT
         + AKST
         + AKDT
         + HST
         + AST

  * -d dss_filename (or --dss dss_filename) - specifies storing data to a 
       HEC-DSS file. dss_filename specifies the HEC-DSS file to use. Relative
       filenames are relative to the working directory.

  * --tzdss dss_time_zone - specifies time zone to use for data stored to a 
       HEC-DSS file. If not specified, the data will be stored to the HEC-DSS
       file in the time zone specified in the USGS text. Valid values for 
       dss_time_zone are valid shef_time_zone values plus any valid Java time
       zone ID (https://en.wikipedia.org/wiki/List_of_tz_database_time_zones).

  * -c (or --cwms) - specifies storing data to a CWMS Oracle database

  * --rule store_rule - specifies CWMS store rule to use for data stored to a 
      CWMS Oracle database. If not specified, DELETE INSERT will be used. 
      Valid values for store_rule are:
         + REPLACE ALL
         + DO NOT REPLACE
         + REPLACE WITH MISSING VALUES ONLY
         + REPLACE WITH NON MISSING
         + DELETE INSERT

  * -h hours_to_retrieve (or --hours hours_to_retreieve) - specifies the number
       of hours of data to retrieve from the USGS. Defaults to 24 hours. Only
       zero, one, or two of -h, -b, and -e must be specified. If none of them or
       only -h is specified, the time window will end at the current time.
	   
  * -b begin_retrieve_date (or --begindate begin_retrieve_date) - specifies the
       beginning of the time window for which to retrieve data from the USGS, in
       the specified or default time zone. If -b is not specified, the beginning
       of the time window is determined by the -h and -e options or their 
       defaults. The format is any date or date/time format recognized by the
       HEC library. If a date only is specified, the time is interpreted as
       00:00 of the specified day. Only zero, one, or two of -h, -b, and -e must
       be specified.
       Examples: (case insensitive and time portion may be omitted)
         + June 2, 2015 14:00
         + June 2, 15 14:00
         + Jun 2, 2015 14:00
         + Jun 2, 15 14:00
         + 2 June 2015 14:00
         + 2 June 15 14:00
         + 02Jun2015 14:00
         + 02Jun15 14:00
         + 2Jun2015 14:00
         + 2Jun15 14:00                                                
         + 02 Jun 2015 14:00
         + 02 Jun 15 14:00
         + 2 Jun 2015 14:00
         + 6/2/15 14:00
         + 6/2/2015 14:00
         + 6-2-15 14:00
         + 6-2-2015 14:00
         + 06/02/15 14:00
         + 06/02/2015 14:00
         + 06-02-15 14:00
         + 06-02-2015 14:00
         + 2015-06-02 14:00 
  
  * -e end_retrieve_date (or --enddate end_retrieve_date) - specifies the end of
       the time window for which to retrieve data from the USGS, in the
       specified or default time zone. If -e is not specified, it will default
       the current time unless both -b and -h are specified, in which case it 
       will default to the specified number of hours after the beginning of the
       time window. The format is any date or date/time format recognized by the
       HEC library. If a date only is specified, the time is interpreted as
       24:00 of the specified day. Only zero, one, or two of -h, -b, and -e must
       be specified. See -b for examples.

  * -z input_time_zone (or --timezone input_time_zone) - specifies the time 
       zone for the -b and -e options. If neither -b or -e are specified this
       has no effect. Defaults to the local time zone. Time zones with or
       without a Daylight Saving Time offset may be specified. Valid values for
       input_time_zone are valid shef_time_zone values plus any valid Java time
       zone ID (https://en.wikipedia.org/wiki/List_of_tz_database_time_zones).

  * -o output_level (or --output output_level) - specifies the level of output
       generated by the program. Defaults to NORMAL. Valid values for 
       output_level are:
         + NONE
         + NORMAL
         + VERBOSE

  * -f (or --forget) - forget stored information about locations that were
       marked as "not found" in previous executions of the program
       
  * -i input_filename (or --input input_filename) - specifies a file name to use
       as input instead of using the USGS NWIS web sites. If this option is
       used, any value specified with -h or --hours is ignored, and the entire
       input file is processed. 

  * -w working_directory (or --workdir working_directory) - specifies the
       working directory for the program. Any relative filenames specified are
       relative to this directory. If not specified, the current directory is
       used as the working directory.

More information can be found at: https://cwms.usace.army.mil/dokuwiki/doku.php?id=usgs_data_retrieval:getusgs
         
'''
changeLog = '''
2.9.3  19-JUL-2018  MBM  Added Timezone of Puerto Rico: 
                         "AST"  : {"SHEF" : "AS", "JAVA" : "Etc/GMT+4" }

2.9.2  20-MAR-2018  MBM  Added an agencies variable as a list to the program defaults 
                         section. The list currently contains USGS and USCE. There are 
                         some gages on the USGS site that are not owned by the USGS 
                         and requires a separate agency_cd field. (An Example USCE gage url: 
                         https://waterdata.usgs.gov/il/nwis/uv?site_no=370000089094501).

2.9.1  19-MAR-2018  MBM  Added Exception Handler to cwmsTs.store method to pass the 
                         exception and move on to the next USGS station. This was done 
                         to handle a UTC offset error causing the script to crash at SAM. 
                         Error reported by Scott Chodkiewicz. This change also required 
                         adding logic to the success[] and haserrors[] output lists 
                         within the processLocation() method.

2.9.0  08-NOV-2017  MDP  Added optional TS_IDS column to the locations file to
                         restrict the SHEF, DSS, or CWMS storage to one or more
                         TS_IDs in the USGS data. Some sites have multiple
                         TS_IDs (which have replaced the DDs mentioned in the
                         2.7 notes) for the same parameter code. Using the
                         columns added in 2.7 allows processing the different
                         TS_IDs into specified sub-location or sub-parameters,
                         where using the TS_IDS column requires no sub-location
                         or sub-parameter. To restrict storage to a specific
                         TS_ID and use a sub-location or sub-parameter, use the
                         TS_IDS column in combination with the appropriate 2.7 
                         column.
                         
                         Modified to allow zero, one, or two of -h, -b, and -e
                         to be used to define the time window.
                         
                         Expanded the formats accepted for -b and -e.
                         
                         Modified to allow times (in addition to dates) to be
                         specified for -b and -e.
                         
                         Added the optional specification of a time zone to be
                         used with -b and -e.
                         
                         Changed URI used to current USGS endpoint when neither
                         -b or -e is used.
                         
2.8.0  04-SEP-2017  MBM  Added parameters for an optional absolute start and end
                         time to be user specified: -b and -e.

2.7.5  04-NOV-2016  MDP  Fixed bug using CWMS and DSS sub-locations.

2.7.4  17-AUG-2016  MDP  Extended previous accommodation to sub-locations and
                         sub-parameters.

2.7.3  09-AUG-2016  MDP  Modified to accommodate new USGS data format.

2.7.2  02-JUN-2016  MDP  Modified to strip carriage return ('\r') characters
                         from .csv files and input file.
                         
                         Modified to skip .csv file lines with empty first
                         field.
                         
                         Fixed small documentation bug.

2.7.1  21-MAY-2013  MDP  Fixed bug in use of -w (--workdir) option

2.7    20-MAY-2013  MDP  Added the following optional columns to the locations
                         file in order to handle multiple instances of the same
                         parameter. Each column takes a comma-separated list of
                         DD=Value pairs, where DD is the USGS Data Descriptor
                         and is the first 2 characters of the parameter
                         descriptor (separated from the parameter code by an 
                         underscore ['_'] character).
                            SHEF_PARAMETER_OVERRIDES
                            DSS_SUB-LOCATIONS
                            DSS_SUB-PARAMETERS
                            CWMS_SUB-LOCATIONS
                            CWMS_SUB-PARAMETERS

2.6.1  13-MAR-2012  MDP  Changed to day-based URL for anything over 120 hours
                    due to USGS site change.

2.6    06-DEC-2011  MDP  Added working directory option.

2.5    09-FEB-2011  MDP  Added input from file option.
                         Optimized logging for huge messages.
                       
2.4.2  02-AUG-2010  MDP  Cleaned up code from previous revisions.
                       
2.4.1  30-JUL-2010  MDP  Corrected output of SHEF location identifier.
                       
2.4    30-JUL-2010  MDP  Modified to correctly handle multiple-interval output
                         from USGS (e.g., sites with 15-, 30- and 60-minute
                         data).
                       
2.3    30-JUL-2010  MDP  Modified to keep track of which locations are not found
                         on the USGS site.  Added -f (--forget) option.
                       
2.2    29-JUL-2010  MDP  Modified time zone handling to read USGS time zone from
                         data records instead of header records
                       
2.1    28-JUL-2010  MDP  Modified command line handling

2.0    26-JUL-2010  MDP  Major update. Moved parameters and aliases from script
                         to input files. Added output of USGS RDB format and
                         storing to DSS & Oracle 
                       
1.0    03-AUG-2005  MDP  Initial version.  Uses input file from HEC-DSSVue
                         plugin. Outputs SHEF messages only
'''
from hec.data import Interval
from hec.heclib.dss import HecDss
from hec.heclib.util import Heclib, HecTime
from hec.io import TimeSeriesContainer
from hec.script import Constants
from java.lang import System
from java.text import SimpleDateFormat
from java.util import Calendar, TimeZone
import anydbm
import array
import getopt
import os
import urllib
import string
import StringIO
import sys
import time
import types
import operator
#-------------#
# "constants" #
#-------------#
A,B,C,D,E,F = 1,2,3,4,5,6
IRREGULAR_INTERVAL = -1
USGS_TEXT, SHEF_TEXT, DSS_FILE, CWMS_DB = 1, 2, 4, 8
NONE, NORMAL, VERBOSE = 0, 1, 2
URL_TEMPLATE_REL = "https://waterservices.usgs.gov/nwis/iv/?format=rdb,1.0&site=%s&period=PT%dH"
URL_TEMPLATE_ABS = "https://waterservices.usgs.gov/nwis/iv/?format=rdb,1.0&site=%s&startDT=%s&endDT=%s"
#------------------#
# program defaults #
#------------------#
programVersion     = "2.9.3"
programDate        = "19-JUL-2018"
programName        = os.path.abspath(sys.argv[0])
programDir         = os.path.dirname(programName)
dbmFilename        = os.path.join(programDir, "getUsgs.notfound")
locationsFilename  = "Locations.csv"
parametersFilename = "Parameters.csv"
paramAliasFilename = "Parameter_Aliases.csv"
usgsSpec      = None
dssspec       = None
shefSpec      = None
cwmsSpec      = None
shefTimezone  = None
dssFilename   = None
dssTimezone   = None
inputFilename = None
storeRule     = "DELETE INSERT"
outputFormat  = NONE
outputLevel   = NORMAL
dfltHourCount = 24
hourCount     = None
forget        = False
workdir       = None
beginTime     = None
endTime       = None
timeZone      = TimeZone.getDefault()
agencies      = ["USGS", "USCE"]
#-----------------------#
# other initializations #
#-----------------------#
startTime = time.time()
dssfile  = None
dbconn   = None
dboffice = None
errorLines = []
notfoundDb = anydbm.open(dbmFilename, "c")
storeToCwmsDbSuccessful = None
successful, nodata, notfound, haserror = [], [], [], []
storeRules = [
    "REPLACE ALL",
    "DO NOT REPLACE",
    "REPLACE MISSING VALUES ONLY", 
    "REPLACE WITH NON MISSING", 
    "DELETE INSERT",
]
tzInfo = {
    "GMT"  : {"SHEF" : "Z",  "JAVA" : "UTC"       },
    "UTC"  : {"SHEF" : "Z",  "JAVA" : "UTC"       },
    "Z"    : {"SHEF" : "Z",  "JAVA" : "UTC"       },
    "EST"  : {"SHEF" : "ES", "JAVA" : "Etc/GMT+5" },
    "EDT"  : {"SHEF" : "ED", "JAVA" : "Etc/GMT+4" },
    "CST"  : {"SHEF" : "CS", "JAVA" : "Etc/GMT+6" },
    "CDT"  : {"SHEF" : "CD", "JAVA" : "Etc/GMT+5" },
    "MST"  : {"SHEF" : "MS", "JAVA" : "Etc/GMT+7" },
    "MDT"  : {"SHEF" : "MD", "JAVA" : "Etc/GMT+6" },
    "PST"  : {"SHEF" : "PS", "JAVA" : "Etc/GMT+8" },
    "PDT"  : {"SHEF" : "PD", "JAVA" : "Etc/GMT+7" },
    "AKST" : {"SHEF" : "LS", "JAVA" : "Etc/GMT+9" },
    "AKDT" : {"SHEF" : "LD", "JAVA" : "Etc/GMT+8" },
    "HST"  : {"SHEF" : "HS", "JAVA" : "Etc/GMT+10"},
    "AST"  : {"SHEF" : "AS", "JAVA" : "Etc/GMT+4" }
}
timezoneNames = tzInfo.keys()
timezoneNames.sort()
#--------------------------#
# process the command line #
#--------------------------#
cmdlineOpts = {
    "locationsfile"  : {"short" : "l:", "long" : "locations=" },
    "parametersfile" : {"short" : "p:", "long" : "parameters="},
    "aliasfile"      : {"short" : "a:", "long" : "aliases="   },
    "usgsspec"       : {"short" : "u",  "long" : "usgs"       },
    "shefspec"       : {"short" : "s",  "long" : "shef"       },
    "cwmsspec"       : {"short" : "c",  "long" : "cwms"       },
    "dssfile"        : {"short" : "d:", "long" : "dss="       },
    "hours"          : {"short" : "h:", "long" : "hours="     },
    "output"         : {"short" : "o:", "long" : "output="    },
    "tzshef"         : {"short" : "",   "long" : "tzshef="    },
    "tzdss"          : {"short" : "",   "long" : "tzdss="     },
    "storerule"      : {"short" : "",   "long" : "rule="      },
    "forget"         : {"short" : "f",  "long" : "forget"     },
    "inputfile"      : {"short" : "i:", "long" : "input="     },
    "workdir"        : {"short" : "w:", "long" : "workdir="   },
    "begindate"      : {"short" : "b:", "long" : "begindate=" },
    "enddate"        : {"short" : "e:", "long" : "enddate="   },
    "timezone"       : {"short" : "z:", "long" : "timezone="  },
}
cmdlineKeys = sorted(cmdlineOpts.keys())
shortopts = "".join([cmdlineOpts[k]["short"] for k in cmdlineKeys if cmdlineOpts[k]["short"]])
longopts = [cmdlineOpts[k]["long"] for k in cmdlineKeys if cmdlineOpts[k]["long"]]
cmdlineSpecs = {}
opts, args = [], []
try :
    opts, args = getopt.getopt(sys.argv[1:], shortopts, longopts)
except Exception, e:
    errorLines.append("Invalid command line: %s" % str(e))
for opt, val in opts :
    for k in cmdlineKeys :
        if opt.strip("-") in map(lambda s : s.strip("=:"), cmdlineOpts[k].values()) :
            cmdlineSpecs[k] = val.strip("=")
            break
if args :
    errorLines.append("Unexpected command line argument(s): %s" % ",".join(args))
#---------------------------------------------#
# override program defaults from command line #
#---------------------------------------------#
if cmdlineSpecs.has_key("locationsfile")  : locationsFilename  = cmdlineSpecs["locationsfile"]        
if cmdlineSpecs.has_key("parametersfile") : parametersFilename = cmdlineSpecs["parametersfile"]        
if cmdlineSpecs.has_key("aliasfile")      : paramAliasFilename = cmdlineSpecs["aliasfile"]        
if cmdlineSpecs.has_key("usgsspec")       : usgsSpec           = cmdlineSpecs["usgsspec"] 
if cmdlineSpecs.has_key("dssfile")        : dssFilename        = cmdlineSpecs["dssfile"]        
if cmdlineSpecs.has_key("shefspec")       : shefSpec           = cmdlineSpecs["shefspec"] 
if cmdlineSpecs.has_key("cwmsspec")       : cwmsSpec           = cmdlineSpecs["cwmsspec"] 
if cmdlineSpecs.has_key("hours")          : hourCount          = cmdlineSpecs["hours"] 
if cmdlineSpecs.has_key("output")         : outputLevel        = cmdlineSpecs["output"].upper()
if cmdlineSpecs.has_key("tzshef")         : shefTimezone       = cmdlineSpecs["tzshef"].upper()
if cmdlineSpecs.has_key("tzdss")          : dssTimezone        = cmdlineSpecs["tzdss"].upper()
if cmdlineSpecs.has_key("storerule")      : storeRule          = cmdlineSpecs["storerule"].upper()
if cmdlineSpecs.has_key("forget")         : forget             = True
if cmdlineSpecs.has_key("inputfile")      : inputFilename      = cmdlineSpecs["inputfile"]        
if cmdlineSpecs.has_key("workdir")        : workdir            = cmdlineSpecs["workdir"]
if cmdlineSpecs.has_key("begindate")      : beginTime          = cmdlineSpecs["begindate"]
if cmdlineSpecs.has_key("enddate")        : endTime            = cmdlineSpecs["enddate"]
if cmdlineSpecs.has_key("timezone")       : timeZone           = TimeZone.getTimeZone(cmdlineSpecs["timezone"])
#-----------------#
# process workdir #
#-----------------#
if workdir is None : workdir = programDir
workdir = os.path.abspath(workdir)
if not os.path.isabs(locationsFilename)  : locationsFilename  = os.path.join(workdir, locationsFilename)
if not os.path.isabs(parametersFilename) : parametersFilename = os.path.join(workdir, parametersFilename)
if not os.path.isabs(paramAliasFilename) : paramAliasFilename = os.path.join(workdir, paramAliasFilename)
if dssFilename :
    if not os.path.isabs(dssFilename) : dssFilename = os.path.join(workdir, dssFilename)
if inputFilename :
    if not os.path.isabs(inputFilename) : inputFilename = os.path.join(workdir, inputFilename)
#---------------------------------#
# setup for input time processing #
#---------------------------------#
cal = Calendar.getInstance()
sdfHecTime = SimpleDateFormat("ddMMMyyyy, HH:mm")
sdfIso8601 = SimpleDateFormat("yyyy-MM-dd'T'HH:mmX")
for sdf in sdfHecTime, sdfIso8601 : sdf.setTimeZone(timeZone)
#-----------------------------#
# validate command line specs #
#-----------------------------#
if type(outputLevel) == types.StringType :
    if outputLevel not in ("NONE", "NORMAL", "VERBOSE") :
        errorLines.append("Invalid output level (%s), must be NONE, NORMAL, or VERBOSE ")
    outputLevel = eval(outputLevel)
if not locationsFilename :
    errorLines.append("Locations file parameter specified without file name")    
elif not os.path.exists(locationsFilename) or not os.path.isfile(locationsFilename) :
    errorLines.append("Locations file does not exist: %s" % locationsFilename)    
if not parametersFilename :
    errorLines.append("Parameters file parameter specified without file name")    
elif not os.path.exists(parametersFilename) or not os.path.isfile(parametersFilename) :
    errorLines.append("Parameters file does not exist: %s" % parametersFilename)    
if not paramAliasFilename :
    errorLines.append("Parameter alias file parameter specified without file name")    
elif not os.path.exists(paramAliasFilename) or not os.path.isfile(paramAliasFilename) :
    errorLines.append("Parameter alias file does not exist: %s" % paramAliasFilename)
if dssFilename is not None :
    outputFormat |= DSS_FILE    
    if os.path.exists(dssFilename) and not os.path.isfile(dssFilename) :
        errorLines.append("DSS parameter specified with invalid file name")
if usgsSpec is not None :
    outputFormat |= USGS_TEXT    
if shefSpec is not None :
    outputFormat |= SHEF_TEXT
if cwmsSpec is not None :
    outputFormat |= CWMS_DB
if shefTimezone is not None and shefTimezone not in timezoneNames :
    errorLines.append("SHEF time zone (%s) not in valid time zones (%s)" % (shefTimezone, ",".join(timezoneNames)))
if storeRule is not None and storeRule not in storeRules :
    errorLines.append("CWMS store rule (%s) not in valid store rules (%s)" % (storeRule, ",".join(storeRules)))
if hourCount is None :
    hourCount = dfltHourCount
else :    
    if beginTime is not None and endTime is not None :
        errorLines.append("Can specify only zero, one, or two of hours, begindate, and enddate - all three are specified")
    else :
        try : 
            hourCount = int(hourCount)
        except : 
            errorLines.append("Invalid hour count parameter: %s" % hourCount)
        else :
            if hourCount < 1 :
                errorLines.append("Hour count (%d) must be greater than 0")
if beginTime is not None :
    t = HecTime()
    try :
        if t.set(beginTime) != 0 : raise Exception
        if not t.isTimeDefined() : t.set("%s 00:00" % beginTime)
        cal.setTime(sdfHecTime.parse(t.dateAndTime(4)))
        beginTime = sdfIso8601.format(cal.getTime())
    except :
        errorLines.append("Invalid beginddate format: %s" % beginTime)
if endTime is not None :
    t = HecTime()
    try :
        if t.set(endTime) != 0 : raise Exception
        if not t.isTimeDefined() : t.set("%s 24:00" % endTime)
        cal.setTime(sdfHecTime.parse(t.dateAndTime(4)))
        endTime = sdfIso8601.format(cal.getTime())
    except :
        errorLines.append("Invalid endddate format: %s" % endTime)
if not outputFormat :
    errorLines.append("No output format(s) specified")
if inputFilename is not None :
    if not os.path.isfile(inputFilename) :
        errorLines.append("Invalid input file specified")
if not os.path.isdir(workdir) :
    errorLines.append("Invalid working directory specified")
    
if errorLines :
    sys.stderr.write(__doc__)
    sys.stderr.write("***\n")
    for errorLine in errorLines :
        sys.stderr.write("*** ERROR : %s\n" % errorLine)        
    sys.stderr.write("***\n")
    System.exit(-1)
os.chdir(workdir)
#-----------------------#
# normalize time window #
#-----------------------#
if beginTime and not endTime :
    cal.setTime(sdfIso8601.parse(beginTime))
    cal.add(Calendar.HOUR_OF_DAY, hourCount)
    endTime = sdfIso8601.format(cal.getTime())
elif endTime and not beginTime :    
    cal.setTime(sdfIso8601.parse(endTime))
    cal.add(Calendar.HOUR_OF_DAY, -hourCount)
    beginTime = sdfIso8601.format(cal.getTime())
#----------------------#
# function definitions #
#----------------------#
class Logger :
    def __init__(self) :
        self.lastnewline = True
        
    def output(self, text, newline=True) :
        buf = StringIO.StringIO()
        linesSkipped = 0
        for c in text :
            if c != "\n" : break
            linesSkipped += 1
        buf.write("\n" * linesSkipped)
        for line in text[linesSkipped:].split("\n") :
            if self.lastnewline :
                buf.write(time.ctime() + " : ")
            buf.write(line + "\n")
        output = buf.getvalue()
        buf.close()
        if not newline :
            sys.stderr.write(output[:-1])
        else :
            sys.stderr.write(output)
        self.lastnewline = newline
        
log = Logger()

def fmtFloat(v) :
    '''
    Format a floating-point to remove trailing zeros after decimal
    '''
    val = "%f" % (v)
    if val.find(".") != -1 :
        while val[-1] == '0' : val = val[:-1]
        if val[-1] == '.' : val = val[:-1]
    return val

def parseCsv(line) :
    quoteChar = None
    chars = list(zip(*line)[0])
    for i in range(len(line)) :
        if chars[i] in '\'"' :
            if quoteChar :
                if chars[i] == quoteChar : quoteChar = None
            else : 
                quoteChar = chars[i]
        elif chars[i] == ',' and not quoteChar :
            chars[i] = '\0'
    fields = ''.join(chars).replace('"', '').split('\0')
    for i in range(len(fields)) :
        if len(fields[i]) > 0 and fields[i][0] == '[' and fields[i][-1] == ']' :
            fields[i] = fields[i][1:-1]
    return fields
            
def outputShefRecord(record, maxLen = 80) :
    '''
    Output as shef record, splitting it as necessary
    '''
    recordType = record[1]
    i = 0
    while len(record) > maxLen :
        i += 1
        last = record[:maxLen].rfind("/")
        last += 1
        sys.stdout.write("%s\n" % record[:last])
        record = ".%s%d %s" % (recordType, i % 10, record[last:])
    sys.stdout.write("%s\n" % record)
    sys.stdout.flush()

def getData(station, seq=None, total=None) :
    '''
    Get the rdb-formatted table from the USGS
    '''
    if beginTime and endTime :
        url = URL_TEMPLATE_ABS % (station, beginTime, endTime)
    else:
        url = URL_TEMPLATE_REL % (station, hourCount)
    if outputLevel > NONE :
        if seq and total :
            log.output("URL= %s" % url)
            log.output("\nRetrieving data for station %s (%d of %d)" % (station, seq, total))
        else :
            log.output("\nRetrieving data for station %s" % station)
        if outputLevel > NORMAL :
            log.output("URL= %s" % url)
    connection = urllib.urlopen(url)
    data = connection.read()
    connection.close()
    return data

def storeToCwmsDb(station, interval, tz, records, decodeInfo) :
    global dbconn, locations, parameters, JdbcConnection, CwmsTsJdbc, storeToCwmsDbSuccessful

    #-----------------------------------------#    
    # delay CWMS imports until they're needed #
    #-----------------------------------------#    
    try    : dir(CwmsTsJdbc)
    except : from cwmsdb import CwmsTsJdbc
    try    : dir(JdbcConnection)
    except : from wcds.dbi.client import JdbcConnection

    if not dbconn : dbconn = JdbcConnection.getConnection()
    cwmsTs = CwmsTsJdbc(dbconn)
    paramInfo, decodeInfo = decodeInfo
    usgsTsid, paramName = paramInfo
    location = locations[station]["CWMS_LOC"]
    try    : location += "-%s" % locations[station]["CWMS_SUB-LOCATIONS"][usgsTsid]
    except : pass
    version  = locations[station]["CWMS_VER"]
    factor = decodeInfo["CWMS_FACTOR"]
    unit   = decodeInfo["CWMS_UNIT"]
    param  = decodeInfo["CWMS_PARAMETER"]
    try    : param += "-%s" % locations[station]["CWMS_SUB-PARAMETERS"][usgsTsid]
    except : pass
    paramType  = decodeInfo["CWMS_TYPE"]
    if interval == IRREGULAR_INTERVAL :
        intvl = "0"
    else :
        intvl = Interval(interval).getInterval()
    if paramType == "Inst" :
        duration = "0"
    else :
        duration = intvl
    cwmsTsid = "%s.%s.%s.%s.%s.%s" % (location, param, paramType, intvl, duration, version)
    times, values, quality = [], [], None
    for j in range(len(records)) :
        millis, value = records[j]
        try    : values.append(float(value) * factor)
        except : pass
        else   : times.append(millis)
    if outputLevel > NONE : log.output("Storing %s (%d values)" % (cwmsTsid, len(values)))
    
    try:
      cwmsTs.store(dboffice, cwmsTsid, unit, array.array('l',times), array.array('d',values), quality, len(values), storeRule, False, None)
      storeToCwmsDbSuccessful = True
      log.output("*** Saved record: %s to CWMS Database. ***" % cwmsTsid)
    except: 
      log.output("*** Unable to Save record: %s to CWMS Database. ***" % cwmsTsid)
      storeToCwmsDbSuccessful = False
    return storeToCwmsDbSuccessful  

def storeToDss(_tsc, station, decodeInfo) :
    global dssFilename, dssfile, locations, parameters
    
    if not dssfile :
        Heclib.zset("MLVL", "", 0) 
#         Heclib.zset("DSSV", "", 6)
        dssfile = HecDss.open(dssFilename)
    paramInfo, decodeInfo = decodeInfo
    tsid, paramName = paramInfo
    parts = ["" for i in range(8)]
    parts[A] = locations[station]["DSS_A-PART"]
    parts[B] = locations[station]["DSS_B-PART"]
    try    : parts[B] += "-%s" % locations[station]["DSS_SUB-LOCATIONS"][tsid]
    except : pass
    parts[F] = locations[station]["DSS_F-PART"]
    tsc = _tsc.clone()
    parts[C] = decodeInfo["DSS_PARAMETER"]
    try    : parts[C] += "-%s" % locations[station]["DSS_SUB-PARAMETERS"][tsid]
    except : pass
    if tsc.interval == IRREGULAR_INTERVAL :
        parts[E] = "IR-MONTH"
    else :
        parts[E] = Interval(tsc.interval).getInterval().upper().replace("S","").replace("MINUTE","MIN").replace("MONTH","MON")
    tsc.units = decodeInfo["DSS_UNIT"]
    tsc.type  = decodeInfo["DSS_TYPE"]
    tsc.fullName = "/".join(parts)
    tsc.watershed = parts[A]
    try    : tsc.location, tsc.subLocation = parts[B].split("-", 1)
    except : tsc.location = parts[B]
    try    : tsc.parameter, tsc.subParameter = parts[C].split("-", 1)
    except : tsc.parameter = parts[B]
    tsc.fileName = dssFilename
    if outputLevel > NONE : log.output("Storing %s:%s (%d values)" % (tsc.fileName, tsc.fullName, tsc.numberValues))
    dssfile.put(tsc)

def makeTimeSeriesContainer(station, interval, tz, records, decodeInfo) :
    global timezones
    sdf = SimpleDateFormat("ddMMMyyyy, HH:mm")
    if dssTimezone :
        if not timezones["DSS"] :
            if tzInfo.hasKey(dssTimezone) :
                timezones["DSS"] = TimeZone.getTimeZone(tzInfo[dssTimezone]["JAVA"])
            else :
                timezones["DSS"] = TimeZone.getTimeZone(dssTimezone)
                if timezones["DSS"].getID() != dssTimezone and outputLevel > NONE : 
                    log.output("WARNING: Couldn't set DSS time zone to %s, using %s" % (dssTimezone,timezones["DSS"].getID()))
                if timezones["DSS"].observesDaylightTime() and outputLevel > NONE :
                    log.output("WARNING: DSS time zone observes daylight saving time")
        sdf.setTimeZone(timezones["DSS"])
    else :
        sdf.setTimeZone(timezones["USGS"])
    decodeInfo = decodeInfo[1]
    cal = Calendar.getInstance()
    t = HecTime()
    tsc = TimeSeriesContainer()
    tsc.interval = interval
    times = []
    values = []
    tsc.quality = None
    factor = decodeInfo["DSS_FACTOR"]
    for j in range(len(records)) :
        millis, value = records[j]
        cal.setTimeInMillis(millis)
        t.set(sdf.format(cal.getTime()))
        times.append(t.value())
        try    : values.append(float(value) * factor)
        except : values.append(Constants.UNDEFINED)
    tsc.times = times
    tsc.values = values
    tsc.startTime = times[0]
    tsc.endTime = times[-1]
    tsc.numberValues = len(values)
    tsc.timeZoneID = sdf.getTimeZone().getID()
    tsc.timeZoneRawOffset = sdf.getTimeZone().getRawOffset()
    return tsc
    
def outputShefText(station, interval, tz, records, decodeInfo) :
    '''
    Output the rdb-formatted data retrieved from the USGS
    '''
    global locations, timezones
    paramInfo, decodeInfo = decodeInfo
    tsid, paramName = paramInfo
    cal = Calendar.getInstance()
    sdfDate = SimpleDateFormat("yyyyMMdd")
    sdfTime = SimpleDateFormat("HHmm")
    if shefTimezone :
        tz = tzInfo[shefTimezone]["SHEF"]
        if not timezones["SHEF"] :
            timezones["SHEF"] = TimeZone.getTimeZone(tzInfo[shefTimezone]["JAVA"])
        for sdf in (sdfDate, sdfTime) : sdf.setTimeZone(timezones["SHEF"])
    else :
        for sdf in (sdfDate, sdfTime) : sdf.setTimeZone(timezones["USGS"])
        
    recordCount = len(records)
    if interval == IRREGULAR_INTERVAL :
        for i in range(recordCount) :
            cal.setTimeInMillis(records[i][0])
            record = ".A %s %8s" % (locations[station]["SHEF_LOC"], sdfDate.format(cal.getTime()))
            record += " %s DH%4s /" % (tzInfo[tz]["SHEF"], sdfTime.format(cal.getTime()))
            try    : param = locations[station]["SHEF_PARAMETER_OVERRIDES"][tsid]
            except : param = decodeInfo["SHEF_PARAMETER"]
            factor = decodeInfo["SHEF_FACTOR"]
            unitSystem = "ES"[decodeInfo["SHEF_UNIT"]]
            try :
                record += " DU%s / %s %s /" % (unitSystem, param, fmtFloat(float(records[i][1]) * factor))
            except :
                record += " %s M /" % (param)
            outputShefRecord(record)
    else :
        cal.setTimeInMillis(records[0][0])
        try    : param = locations[station]["SHEF_PARAMETER_OVERRIDES"][tsid]
        except :  param = decodeInfo["SHEF_PARAMETER"]
        factor = decodeInfo["SHEF_FACTOR"]
        unitSystem = "ES"[decodeInfo["SHEF_UNIT"]]
        record = ".E %s %8s" % (locations[station]["SHEF_LOC"], sdfDate.format(cal.getTime()))
        record += " %s DH%4s / DU%s / %s /" % (tzInfo[tz]["SHEF"], sdfTime.format(cal.getTime()), unitSystem, param)
        if interval % 60 :
            record += " DIN+%2.2d /" % interval
        else :
            record += " DIH+%2.2d /" % (interval / 60)
        for j in range(recordCount) :
            try :
                record += " %s /" % fmtFloat(float(records[j][1]) * factor)
            except :
                record += " M /"
        outputShefRecord(record)

def processLocation(location, locationInfo, seq=None, total=None) :

    global timezones, parameters, successful, notfound, nodata, haserror, storeToCwmsDbSuccessful
    
    if os.path.isfile(location) :
        f = open(location)
        data = f.read().strip().replace('\r', '')
        f.close()
        location = os.path.splitext(os.path.basename(location))[0]
    else :
        data = getData(location, seq, total)
    if not data :
        if outputLevel > NONE : log.output("*** No data ***")
        nodata.append(location)
        return

    tz = ""
    tzField = None
    paramsToOutput = locationInfo["PARAMETERS"]
    
    if outputFormat & USGS_TEXT :
        sys.stdout.write(data)
        
    if data.find("No sites/data found using the selection criteria specified") != -1 :
        if outputLevel > NONE : log.output("*** Site not found ***")
        notfound.append(location)
        notfoundDb[location] = "True"
        return
                
    if outputFormat & (SHEF_TEXT | DSS_FILE | CWMS_DB) :
        if outputLevel > NORMAL :
            log.output("Parsing the following data:\n---------------------------")
            log.output("%s\n" % data)
    
        #------------------------------------------------------------------------------#
        # read through all the comment lines, and find the location name and time zone #
        #------------------------------------------------------------------------------#
        stationText = "#  USGS %s " % location
        lines = data.replace("\r\n", "\n").split("\n")
        for i in range(len(lines)) :
            line = lines[i].strip()
            if not line : continue
            if line[0] == "#" :
                pass
            else :
                break
        else :
            if outputLevel > NONE : log.output("*** No values ***")
            nodata.append(location)
            return
        
        #-----------------------------------------------------#
        # process the 1st header line, describing field names #
        #-----------------------------------------------------#
        fields = lines[i].split()
        fieldCount = len(fields)
        if fieldCount < 3 or " ".join(fields[:3]) != "agency_cd site_no datetime" :
            if outputLevel > NONE :
                log.output("*** Unexpected format on header line 1 ***")
                log.output("%s" % lines[i])
            haserror.append(location)
            return
        paramCount = fieldCount - 3
        if paramCount < 1 :
            if outputLevel > NONE : log.output("*** No parameters ***")
            nodata.append(location)
            return
    
        paramNames = fields[:]
        fieldsToOutput = []
        decodeInfo = []
        for j in range(3, len(paramNames)) :
            if paramNames[j] == "tz_cd" :
                tzField = j
            else :
                tsCode, paramName = paramNames[j].split("_", 1)
                if locationInfo.has_key("TS_IDS") and tsCode not in locationInfo["TS_IDS"] : continue
                if paramName in paramsToOutput :
                    fieldsToOutput.append(j)
                    try :
                        decodeInfo.append(((tsCode, paramName), parameters[paramName]))
                    except :
                        if outputLevel > NONE : log.output("*** Unexpected parameter %s ***" % paramName)
                        haserror.append(location)
                        return
    
        if not fieldsToOutput :
            if outputLevel > NONE : log.output("*** No data ***")
            nodata.append(location)
            return
    
        if not tzField :
            if outputLevel > NONE : log.output("*** No timezone field specified ***")
            haserror.append(location)
            return
        
        #--------------------------#
        # skip the 2nd header line #
        #--------------------------#
        i += 1
    
        #-----------------------------------------------------------------------------#
        # read the data records, keeping track of whether we have regular time-series #
        #-----------------------------------------------------------------------------#
        records = []
        tList = []
        sdf = SimpleDateFormat("yyyy-MM-dd HH:mm")
        cal = Calendar.getInstance()
        recordCount = 0
        for i in range(i+1, len(lines)) :
            if not lines[i].strip() : continue
            fields = lines[i].split("\t")
            if fields[0] not in agencies :
                continue
            if fields[1] != location :
                if outputLevel > NONE :
                    log.output("*** Unexpected location on data record %d ***" % recordCount)
                    if outputLevel > NORMAL :
                        log.output("%s" % lines[i])
                haserror.append(location)
                return
            if not tz :
                tz = fields[tzField]
                timezones["USGS"] = TimeZone.getTimeZone(tzInfo[tz]["JAVA"])
                sdf.setTimeZone(timezones["USGS"])
                if outputLevel > NORMAL :
                    log.output("Initial time zone is %s" % tz)
            else :
                if fields[tzField] != tz :
                    if outputLevel > NORMAL :
                        log.output("Time zone switched from %s to %s" % (tz, fields[tzField]))
                    tz = fields[tzField]
                    timezones["USGS"] = TimeZone.getTimeZone(tzInfo[tz]["JAVA"])
                    sdf.setTimeZone(timezones["USGS"])
            recordCount += 1
            cal.setTime(sdf.parse(fields[2]))
            
            valueFields = []
            for j in fieldsToOutput :
                valueFields.append(fields[j])
            records.append((cal.getTimeInMillis(), valueFields))
            tList.append(cal.getTime())
        if recordCount == 0 :
            if outputLevel > NONE : log.output("*** No data ***")
            nodata.append(location)
            return

        #--------------------------------------------------#
        # create individual time series for each parameter #
        #--------------------------------------------------#
        intvl = [None for i in range(len(fieldsToOutput))]
        ts    = [[] for i in range(len(fieldsToOutput))]
        for i in range(len(records)) :
            millis, values = records[i]
            for j in range(len(values)) :
                if values[j] != "" : ts[j].append((millis, values[j]))
        #--------------------------------------------------------------------#
        # analyze interval for each time series, allowing for missing values #
        #--------------------------------------------------------------------#
        for i in range(len(ts)) :
            intervalCounts = {}
            for j in range(1, len(ts[i])) :
                # 60,000 milliseconds per minute
                intv = (ts[i][j][0] - ts[i][j-1][0]) / 60000
                count = intervalCounts.setdefault(intv, 0)
                intervalCounts[intv] = count + 1
            intvs = intervalCounts.keys()
            intvs.sort()
            if len(intvs) == 0 :
                #------------------------------------------------#
                # not enough values (2) to determine an interval #
                #------------------------------------------------#
                intvl[i] = IRREGULAR_INTERVAL
                log.output("not enough values to determine an interval, setting to: Irregular Interval")
            elif len(intvs) == 1 :
                #---------------------------------#
                # only one interval found in data #
                #---------------------------------#
                intvl[i] = intvs[0]
            else :
                
                if intvl[i] is None :
                    #--------------------------------#
                    # interval still hasn't been set #
                    #--------------------------------#
                                                                                               
                    if intervalCounts[intvs[0]] > 3 * max([intervalCounts[intvs[x]] for x in range(1, len(intvs))]) :
                        #---------------------------------------------------#
                        # smallest interval accounts for > 75% of intervals #
                        #---------------------------------------------------#
                        intvl[i] = intvs[0]
                        log.output("smallest interval accounts for > 75% of data: " + str(intvl[i]))
#                     elif max([intervalCounts[intvs[x]] for x in range(1, len(intvs))]) > (0.75 * len(intvs)) :
#                         #--------------------------------------------------------------------------#
#                         # most common encountered interval accounts for > 75% of intervals, use it #
#                         # and clobber any additional data in between predominant interval          #
#                         #--------------------------------------------------------------------------#
#                         intvl[i] = max(intervalCounts.iteritems(), key=operator.itemgetter(1))[0]
#                         log.output("interval accounts for > 75% of data: " + str(intvl[i]))
                    else:
                        #----------------------------------------------------------------------#
                        # multiple intervals found in data and smallest is not >75% prevailing #
                        #----------------------------------------------------------------------#
                        for j in range(1, len(intvs)) :
#                             print 'intvs[j] % intvs[0]' , intvs[j] % intvs[0]
                            if intvs[j] % intvs[0] :
                                #-------------------------------------------------#
                                # interval is not a multiple of smallest interval #
                                #-------------------------------------------------#
                                intvl[i] = IRREGULAR_INTERVAL
                                log.output("interval found that is not a multiple of smallest interval and no dominant interval found, setting to: Irregular Interval")
#                             elif not intvs[j] % intvs[0] :
#                                 intvl[i] = intvs[0]
#                                 log.output("All intervals are a multiple of smallest interval. Using smallest interval.")
                            else :
                                #------------------------------------------------#
                                # can't determine a predominant regular interval #
                                #------------------------------------------------#
                                intvl[i] = IRREGULAR_INTERVAL
                                log.output("Unable to determine interval, setting to: Irregular Interval")
            
            #------------------------------------------------------------#
            # add in any missing values for regular interval time series #
            #------------------------------------------------------------#
            if intvl[i] != IRREGULAR_INTERVAL :
                for j in range(1, len(ts[i]))[::-1] :
#                     print 'ts[i][j][0]: ', ts[i][j][0]/60000
                    intv = (ts[i][j][0] - ts[i][j-1][0]) / 60000
                    intervalsToAdd = range((ts[i][j-1][0] / 60000) + intvl[i], ts[i][j][0] / 60000, intvl[i])
                    for k in intervalsToAdd[::-1] :
                        ts[i].insert(j, (k * 60000, ""))
                        
            #------------------------------------------------------------------#
            # Remove any values that are not of the chosen interval #
            #------------------------------------------------------------------#
#             if intvl[i] != IRREGULAR_INTERVAL :
#                 intervalsToRemove = None
#                 for j in range(1, len(ts[i]))[::-1] :
#                     intv = (ts[i][j][0] - ts[i][j-1][0]) / 60000
# #                     print 'intv & intvl[i]: ', intv, intvl[i]
#                     if intv != intvl[i]:
#                         #------------------------------------------------------#
#                         # interval is not equal to the chosen regular interval #
#                         #------------------------------------------------------#
#                         intervalsToRemove = range((ts[i][j-1][0] / 60000) + intvl[i], ts[i][j][0] / 60000, intvl[i])
#                         
#                     if intervalsToRemove is not None:
#                         print 'intervalsToRemove : ', intervalsToRemove
# #                     print '\nintv ', intv
#                     
            
                        
        #------------------------------#
        # output and/or store the data #
        #------------------------------#
        for i in range(len(ts)) :
            if not intvl[i] or not ts[i] : continue
            if outputFormat & SHEF_TEXT :
                outputShefText(location, intvl[i], tz, ts[i], decodeInfo[i])
            
            if outputFormat & DSS_FILE : 
                tsc = makeTimeSeriesContainer(location, intvl[i], tz, ts[i], decodeInfo[i])
                storeToDss(tsc, location, decodeInfo[i])
        
            if outputFormat & CWMS_DB  : 
                storeToCwmsDb(location, intvl[i], tz, ts[i], decodeInfo[i])
            
    try:
        if outputFormat & CWMS_DB and storeToCwmsDbSuccessful:  
            log.output("successful list appended.")      
            successful.append(location)
        elif outputFormat & CWMS_DB and not storeToCwmsDbSuccessful: 
            haserror.append(location)
            log.output("haserror list appended.")  
        else: successful.append(location)
    except: pass
#------------------------#
# output run information #
#------------------------#
if outputLevel > NONE :
    log.output("\n=== getUSGS version %s (%s) starting up ===" % (programVersion, programDate))
    if cmdlineSpecs.has_key("timezone") and timeZone.getID() != cmdlineSpecs["timezone"] and beginTime is not None :
        log.output("WARNING: Couldn't set input time zone to %s, using %s" % (dssTimezone,timezones["DSS"].getID()))
    log.output("Using locations file %s" % locationsFilename)
    log.output("Using parameters file %s" % parametersFilename)
    log.output("Using parameter alias file %s" % paramAliasFilename)
    if inputFilename :
        log.output("Retrieving data from input file %s" % inputFilename)
    elif beginTime and endTime :
        log.output("Retrieving data for Start Date = %(x)s and End Date = %(y)s" % {"x" : str(beginTime), "y" : str(endTime)})
    else:
        log.output("Retrieving data for previous %d hours" % hourCount)
    if outputFormat :
        if outputFormat & USGS_TEXT :
            log.output("Outputting USGS text")
        if outputFormat & SHEF_TEXT : 
            if shefTimezone :
                log.output("Outputting SHEF data in %s time zone (SHEF time zone code %s)" % (shefTimezone, tzInfo[shefTimezone]["SHEF"]))
            else :
                log.output("Outputting SHEF data in time zone used by USGS")
        if outputFormat & DSS_FILE :
            if dssTimezone :
                log.output("Outputting to DSS file %s in %s time zone" % (dssFilename, dssTimezone))
            else :
                log.output("Outputting to DSS file %s in time zone used by USGS" % dssFilename)
        if outputFormat & CWMS_DB :
            log.output("Outputting to CWMS database with store rule %s" % storeRule)
#-----------------------------------#
# set up the Java time zones to use #
#-----------------------------------#
timezones = {"USGS" : None, "SHEF" : None, "DSS" : None}
if shefTimezone : 
    timezones["SHEF"] = TimeZone.getTimeZone(tzInfo[shefTimezone]["JAVA"])
if dssTimezone :
    timezones["DSS"] = TimeZone.getTimeZone(tzInfo[dssTimezone]["JAVA"])
#-----------------------------------------------#
# read the parameter aliases file, if it exists #
#-----------------------------------------------#
"[USGS_PARAMETER],ALIAS"
parameterAliases = {}
aliasfile = open(paramAliasFilename, 'r')
lines = aliasfile.read().strip().replace('\r', '').split("\n")
aliasfile.close()
parameterAliasKeys = parseCsv(lines[0].upper())
for line in lines[1:] :
        line = line.strip()
        if not line or line.startswith("#") : continue
        fields = parseCsv(line)
        if not fields[0].strip() : continue
        for i in range(1,len(parameterAliasKeys)) :
            if parameterAliasKeys[i] == "ALIAS" :
                parameterAliases[fields[i]] = fields[0]
                break

#---------------------------#
# parse the parameters file #
#---------------------------#
"[USGS_PARAMETER],SHEF_PARAMETER,SHEF_FACTOR,SHEF_UNIT,DSS_PARAMETER,DSS_FACTOR,DSS_UNIT,DSS_TYPE,CWMS_FACTOR,CWMS_UNIT,CWMS_TYPE"
parameters = {}
parametersfile = open(parametersFilename, 'r')
lines = parametersfile.read().strip().replace('\r', '').split('\n')
parametersfile.close()
parameterKeys = parseCsv(lines[0].upper())
for line in lines[1:] :
    line = line.strip()
    if not line or line[0] == '#' : continue
    fields = parseCsv(line)
    if not fields[0].strip() : continue
    parameters[fields[0]] = {}
    for i in range(1,len(parameterKeys)) : 
        if parameterKeys[i].endswith("FACTOR") : 
            fields[i] = float(fields[i]) 
        elif parameterKeys[i] == "SHEF_UNIT" : 
            fields[i] = fields[i].upper() != "ENGLISH"
        parameters[fields[0]][parameterKeys[i]] = fields[i]

#--------------------------#
# parse the locations file #
#--------------------------#
"[USGS_LOC],SHEF_LOC,SHEF_PARAMETER_OVERRIDES,DSS_A-PART,DSS_B-PART,DSS_F-PART,DSS_SUB-LOCATIONS,DSS_SUB-PARAMETERS,CWMS_LOC,CWMS_VER,CWMS_SUB-LOCATIONS,CWMS_SUB-PARAMETERS,PARAMETERS"
if forget :
    for location in notfoundDb.keys() :
        if outputLevel > NORMAL :
            log.output("Forgetting previously not found location %s" % location) 
        del notfoundDb[location]
locations = {}
locationsfile = open(locationsFilename, 'r')
lines = locationsfile.read().strip().replace('\r', '').split('\n')
locationsfile.close()
locationKeys = parseCsv(lines[0].upper())
for line in lines[1:] :
    line = line.strip()
    if not line or line[0] == '#' : continue
    fields = parseCsv(line)
    if not fields[0].strip() : continue
    location = fields[0]
    if notfoundDb.has_key(location) : 
        if outputLevel > NORMAL and not inputFilename:
            log.output("Skipping previously not found location %s" % location) 
        continue
    locations[location] = {}
    for i in range(1, len(locationKeys)) :
        if locationKeys[i] in (
            "SHEF_PARAMETER_OVERRIDES",
            "DSS_SUB-LOCATIONS",
            "DSS_SUB-PARAMETERS",
            "CWMS_SUB-LOCATIONS",
            "CWMS_SUB-PARAMETERS") :
            pairs = fields[i].strip().split(",")
            fields[i] = {}
            for pair in pairs :
                if not pair : continue
                key, value = map(string.strip, pair.split("="))
                if not key.isdigit():
                    raise Exception("Invalid key (%s) in %s column of %s for location %s" % (key, fields[i], locationsFilename, location))
                if fields[i].has_key(key) :
                    raise Exception("Duplicate (%s) in %s column of %s for location %s" % (key, fields[i], locationsFilename, location))
                fields[i][key] = value
            log.output("\n%s : %s" % (locationKeys[i], str(fields[i])))
        elif locationKeys[i] == "PARAMETERS" :
            params = fields[i].split(",")
            fields[i] = []
            for param in params :
                try    : fields[i].append(parameterAliases[param.strip()])
                except : fields[i].append(param.strip())
        elif locationKeys[i] == "TS_IDS" :
            fields[i] = fields[i].split(",")
        locations[location][locationKeys[i]] = fields[i]
#-----------------------#    
# process the locations #
#-----------------------#
if inputFilename :
    retrievalCount = 1
else :
    retrievalCount = len(locations)
i = 0
try :
    if inputFilename :
        location = os.path.splitext(os.path.basename(inputFilename))[0]
        if location not in locations.keys() :
            msg = 'Location "%s" is unknown (taken from input file name "%s")' % (location, inputFilename)
            log.output("\n%s" % msg)
            raise Exception(msg)
        processLocation(inputFilename, locations[location], i, retrievalCount) 
    else :
        for location in locations.keys() :
            i += 1
            processLocation(location, locations[location], i, retrievalCount) 
finally :    
    if dssfile    : dssfile.done()
    if dbconn     : dbconn.close()
    if notfoundDb : notfoundDb.close()
#-----------------------#
# output the statistics #
#-----------------------#
remainingCount = retrievalCount - len(successful) - len(notfound) - len(nodata) - len(haserror)
if outputLevel > NONE :
    log.output("\n%d of %d stations successfully processed" % (len(successful), retrievalCount))
    if len(notfound) > 0 : 
        log.output("\n%d of %d stations were not found" % (len(notfound), retrievalCount))
        if outputLevel > NORMAL :
            for i in range(len(notfound)) :
                loc = notfound[i]
                line = "\t%s" % loc
                if locations[loc].has_key("SHEF_LOC") and locations[loc]["SHEF_LOC"] : line += ", SHEF=%s" % locations[loc]["SHEF_LOC"] 
                if locations[loc].has_key("DSS_B-PART") and locations[loc]["DSS_B-PART"] : line += ", DSS=%s" % locations[loc]["DSS_B-PART"] 
                if locations[loc].has_key("CWMS_LOC") and locations[loc]["CWMS_LOC"] : line += ", CWMS=%s" % locations[loc]["CWMS_LOC"] 
                log.output(line)
    if len(nodata) > 0 : 
        log.output("\n%d of %d stations had no data" % (len(nodata), retrievalCount))
        if outputLevel > NORMAL :
            for i in range(len(nodata)) :
                loc = nodata[i]
                line = "\t%s" % loc
                if locations[loc].has_key("SHEF_LOC") and locations[loc]["SHEF_LOC"] : line += ", SHEF=%s" % locations[loc]["SHEF_LOC"] 
                if locations[loc].has_key("DSS_B-PART") and locations[loc]["DSS_B-PART"] : line += ", DSS=%s" % locations[loc]["DSS_B-PART"] 
                if locations[loc].has_key("CWMS_LOC") and locations[loc]["CWMS_LOC"] : line += ", CWMS=%s" % locations[loc]["CWMS_LOC"] 
                log.output(line)
    if len(haserror) > 0 : 
        log.output("\n%d of %d stations had errors" % (len(haserror), retrievalCount))
        if outputLevel > NORMAL :
            for i in range(len(haserror)) :
                loc = haserror[i]
                line = "\t%s" % loc
                if locations[loc].has_key("SHEF_LOC") and locations[loc]["SHEF_LOC"] : line += ", SHEF=%s" % locations[loc]["SHEF_LOC"] 
                if locations[loc].has_key("DSS_B-PART") and locations[loc]["DSS_B-PART"] : line += ", DSS=%s" % locations[loc]["DSS_B-PART"] 
                if locations[loc].has_key("CWMS_LOC") and locations[loc]["CWMS_LOC"] : line += ", CWMS=%s" % locations[loc]["CWMS_LOC"] 
                log.output(line)
                log.output("\t" + "\t".join([haserror[i], locations[haserror[i]]["SHEF_LOC"], locations[haserror[i]]["DSS_B-PART"], locations[haserror[i]]["CWMS_LOC"]]))
    if remainingCount > 0 :
        log.output("\n%d of %d stations were not attempted due to abort" % (remainingCount, retrievalCount))
    endTime = time.time()
    elapsed = int(endTime - startTime)
    h = elapsed / 3600
    m = (elapsed - 3600 * h) / 60
    s = elapsed % 60
    log.output("\n=== getUSGS version %s (%s) was alive for %2.2d:%2.2d:%2.2d ===" % (programVersion, programDate, h, m, s))
System.exit(0)
