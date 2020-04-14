from hec.script import *
import time
import java

#---------------------#
# some code to eval() #
#---------------------#
getCurrentTimeSnippet = "time.ctime(time.time())"

#-----------------#
# a simple script #
#-----------------#
scriptText = '''
def myFunc() :
	global startTime, endTime
	startTime = time.time()
	for i in range(3) :
		print("Sleeping for 1 second at %f" % time.time())
		time.sleep(1)
	endTime = time.time()

myFunc()	
print("Start time = %s" % time.ctime(startTime))
print("End time   = %s" % time.ctime(endTime))
'''

#--------------------------------#
# write the script out to a file #
#--------------------------------#
scriptFilename = "myFunc.py"
scriptFile = open(scriptFilename, "w")
scriptFile.write(scriptText)
scriptFile.close()

#----------------------------------#
# Use eval() to evaluate some code #
#----------------------------------#
print("\nCalling eval()")
print("The local time is %s" % eval(getCurrentTimeSnippet))

#---------------------------------------#
# set up a separate scope for execution #
#---------------------------------------#
otherGlobals = {"time" : time, "startTime" : None, "endTime" : None}
otherLocals  = {}

#------------------------------------#
# exec some text in a separate scope #
#------------------------------------#
print("\nCalling exec in a separate scope")
exec scriptText in otherGlobals, otherLocals
try    : print("Global variable startTime = %f" % startTime)
except : print("Global variable  startTime is not defined.")
try    : print("Global variable endTime   = %f" % endTime)
except : print("Global variable  endTime is not defined.")

#---------------------------------------------#
#execfile the same script in a separate scope #
#---------------------------------------------#
print("\nCalling execfile in a separate scope")
execfile(scriptFilename, otherGlobals, otherLocals)
try    : print("Global variable startTime = %f" % startTime)
except : print("Global variable  startTime is not defined.")
try    : print("Global variable endTime   = %f" % endTime)
except : print("Global variable  endTime is not defined.")

#-------------------------------------#
# exec the same text in our own scope #
#-------------------------------------#
print("\nCalling exec in the current scope")
exec scriptText
try    : print("Global variable startTime = %f" % startTime)
except : print("Global variable  startTime is not defined.")
try    : print("Global variable endTime   = %f" % endTime)
except : print("Global variable  endTime is not defined.")

#------------------------------------------#
#execfile the same script in our own scope #
#------------------------------------------#
print("\nUndefining global variables startTime and endTime")
del globals()['startTime']
del globals()['endTime']
print("\nCalling execfile in the current scope")
execfile(scriptFilename)
try    : print("Global variable startTime = %f" % startTime)
except : print("Global variable  startTime is not defined.")
try    : print("Global variable endTime   = %f" % endTime)
except : print("Global variable  endTime is not defined.")


