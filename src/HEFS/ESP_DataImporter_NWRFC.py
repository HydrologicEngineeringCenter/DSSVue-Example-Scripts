# name=ESP Data Importer NWRFC
# displayinmenu=true
# displaytouser=true
# displayinselector=true
from  javax.swing		import JOptionPane
from  java.util		import ArrayList
from hec.heclib.dss	import HecDss
from hec.heclib.util 	import HecTime
from hec.hecmath		import TimeSeriesMath
from hec.io			import TimeSeriesContainer
from urllib2 			import urlopen
import csv

def readCSV(fileName):
	data=list(csv.reader(open(fileName)))
	return data

def downloadFile(url,destinationFileName):
	r = urlopen(url)
	data = r.read()
	with open(destinationFileName,'wb') as f:
		f.write(data)

def createTemplateTSC(rawDataList):
	#Derives a TimeSeriesContainer object from the raw ESP data list
	#  where all that needs to be done is update the pathname
	#  and values - timestamps should be uniform across each 
	#  ESP trace
  
	#intializing HEC java objects
	tsc =TimeSeriesContainer() #new TSC object
	hecStartTime=  HecTime()
	hecEndTime =  HecTime()

	#copmuting HEC times and interval (minutes) of timestep
	times = []
	for i in range(len(rawDataList)):
		times.append(rawDataList[i][0])
	hecStartTime.set(times[0])
	hecEndTime.set(times[-1])
	#The formatting of these times might need to be adjusted at a later point

	Dates = []
	for x in range(len(times)):
		IndividualDate = times[x]
		T = HecTime()
		T.set(IndividualDate)
		Dates.append(T.value())

	DiffBetweenInterval = []
	DiffBetweenInterval = [a - Dates[i-1] for i, a in enumerate(Dates)][1:]
	for x in DiffBetweenInterval:
		UniqueList_Minutes = []
		#Check if exist in list or not
		if x not in UniqueList_Minutes:
			UniqueList_Minutes.append(x)
	interval =UniqueList_Minutes[0]
	hecTimes = list(range(Dates[0],Dates[-1],int(interval)))
	hecTimes.append(Dates[-1]) 
	interval_hours = int(interval)/60
	tsc.times = hecTimes
	tsc.values = [0]*len(times) #add null data number here.
	tsc.interval = interval_hours
	tsc.startTime =(int(hecStartTime.julian())*1440)+1080
	tsc.endTime =(int( hecEndTime.julian())*1440)+1080
	tsc.numberValues = len(times)
	tsc.units = "CFS"
	tsc.type = "PER-AVER"
	tsc.parameter =  "FLOW" #Assuming always want this to be flow
	
	return tsc
	
def getESPConfigFromURL(SiteUrl):
	return("natural")
	#This was orginally set using a couple of different options but this code is being written in a way to only return "natural" values
	
	#This is R code, needs to be modified if desired to be used in Jython.
	#rfcLinks$esp_config[rfcLinks$url==siteURL]

def MultValues(CSV_Data, colName):
	Values = []
	TempVal = []
	for i in range(len(CSV_Data)):
		TempValInt = CSV_Data[i]
		MultCol = float(TempValInt)*1000
		Values.append(round(MultCol,2))	
	return Values

def formDSSPath(colName,siteURL):
	#Forms an appropriate DSS file name from the URL and the column name
	#  in the ESP dataframe (e.g., 'X1952')
	#output (e.g.): //ALF/FLOW/01JUL2019/6HOUR/C:001949|WATER_SUPPLY/
	siteID = ESP_TraceOfInterest.rsplit('.',2)[0].rsplit("_",1)[0] #B part
	wy =int( colName)+1 #my in F part
	esp_config = getESPConfigFromURL(siteURL) #esp type in F part
	return("//%s/FLOW//6HOUR/C:%06d|%s/" %( siteID,wy,esp_config.upper()))

def updateTSCfromESP(tsc, values, colName, SiteUrl):
	path = formDSSPath(colName,SiteUrl)
	tsc.values = MultValues(values,colName)
	tsc.fullName = path
	tsc.location = getPathPart(path,"A")
	tsc.watershed = getPathPart(path,"B")
	tsc.version = getPathPart(path,"F")
	return tsc

def AlphaCharacterNum(DSSPart):
	if DSSPart == "A":
		return(1)
	elif DSSPart == "B":
		return(2)
	elif DSSPart == "C":
		return(3)
	elif DSSPart == "D":
		return(4)
	elif DSSPart == "E":
		return(5)
	elif DSSPart == "F":
		return(6)

def getPathPart(path,part): #gets A-F part from DSS path
	partIndex = AlphaCharacterNum(part)
	return(path.split('/')[partIndex])

def GetEnsembleValues(ESP_Matrix,columnToExtract):
	rval=[]
	for i in range(len(ESP_Matrix)):
	        TempESP_Value = ESP_Matrix[i][columnToExtract]	        
	        rval.append(float(TempESP_Value))
	return rval

def GagesToDownload(EspDaysCSV):
	for x in range(len(EspDaysCSV)):
		for i in range(len(GoI_NoSpace)):
			if EspDaysCSV[x][:5].upper == GoI_NoSpace[i][:5].upper:		
				GagesUsed.append(EspDaysCSV[x])
	return GagesUsed
	
def SaveToDSS(rawDataList,SaveLocation,espDays,URLSite):
	 #From raw data list, saves the list of ESP dataframes to file
	#  If saveLocation is a file, saves there.  saveLocation can also
	#  be a directory, in which case a default file name is written provided
	#  the espDays  argument is assigned	
	if SaveLocation[-3:].upper()=='DSS':
		outFileName =  ("%s" %(SaveLocation))
	else:
		outFileName = ("%s\\rfc_esp_flows_%sday.dss" % (SaveLocation,espDays))
	dssFile = HecDss.open(outFileName,1)

	ESP_Matrix = rawDataList[7:] #This is set for NW RFC's data. There is extra meta data that we do not need to parse through

	TimeStamp_Matrix = []
	for i in range(len(ESP_Matrix)):
		TempTimeStampData = ESP_Matrix[i][0]
		TimeStamp_Matrix.append(TempTimeStampData)
	#print(TimeStamp_Matrix)

	EnsembleDataValues = []
	for i in range(len(ESP_Matrix)):
		TempESP_Value = ESP_Matrix[i][1:]
		EnsembleDataValues.append(TempESP_Value)
	
	templateTsc = createTemplateTSC(ESP_Matrix)
	
	#NumMembers is the variable to represent the number of ensemble members. This currently has the minus 1 to remove the initial column that is labeling the second dimision of the data.
	NumMembers = len(ESP_Matrix[0])-1
	#NumTimeSteps is to denote how many time steps are with the data. 
	NumTimeSteps = len(ESP_Matrix)

	for colIndex in range(NumMembers):
		tsc = updateTSCfromESP(tsc = templateTsc, #update tsc object with data for this ESP trace
		                      values = GetEnsembleValues(ESP_Matrix,colIndex+1),
		                      colName = colIndex,
		                      SiteUrl = URLSite)
		dssFile.put(tsc)
	dssFile.done()


#This is to set the file location.
#It allows for the user to choose if they want to use the default open DSS File or if they want to use a different file location.
#choices = ( "User Input", "Same as Open DSS File" )
#DssFileLocation = JOptionPane.showInputDialog(None, "How would you like to denote the DSS file path?","DSS File Path", JOptionPane.QUESTION_MESSAGE, None,  choices, choices[0])
DssFileLocation ="User Input" 
if DssFileLocation == "User Input":
	SaveLocation = JOptionPane.showInputDialog( "Please input a save location (Do not end with '\\')'.\nYou can either put in a DSS file location to specify a name or a file location and a default name will be popualted")
	#SaveLocation = "C:\Users\q0hecajd\Desktop\Temp\Scripts\TestData.dss"
elif DssFileLocation == "Same as Open DSS File":
	None
	#Want this to be able to automatically direct to the open DSS file. 
GagesOfInterest = JOptionPane.showInputDialog( "Please input the gage identifiers (seperate with a common for multiple locations")
#GagesOfInterest = "ABOM8N, AGNO3N, PRPI1N"
GagesOfInterest = GagesOfInterest .rsplit(',',2)

GoI_NoSpace = []
for i in range(len(GagesOfInterest)):
		GoI_NoSpace.append(GagesOfInterest[i].replace( " ",""))
	
#This is for the current location of my test DSS file
EspDaysChoices = ( "0", "10" )
EspDays = JOptionPane.showInputDialog(None, "How many Days of the short-term weather forecast?","ESP Days", JOptionPane.QUESTION_MESSAGE, None,  EspDaysChoices, EspDaysChoices[0])
#EspDays = "0"

print("\n\nBeginning ESP Download\n")

CSV_List_Options_NorthWestRFC = [
'ABOM8N_SQIN.ESPF0.csv','ABOM8N_SQIN.ESPF10.csv','ABOM8N_SQIN.ESPFM.csv','AGNO3N_SQIN.ESPF0.csv','AGNO3N_SQIN.ESPF10.csv','AGNO3N_SQIN.ESPFM.csv','AGSO3N_SQIN.ESPF0.csv','AGSO3N_SQIN.ESPF10.csv','AGSO3N_SQIN.ESPFM.csv','ALBO3N_SQIN.ESPF0.csv','ALBO3N_SQIN.ESPF10.csv','ALBO3N_SQIN.ESPFM.csv','ALFW1IN_SQIN.ESPF0.csv','ALFW1IN_SQIN.ESPF10.csv','ALFW1IN_SQIN.ESPFM.csv','ALPW4N_SQIN.ESPF0.csv','ALPW4N_SQIN.ESPF10.csv','ALPW4N_SQIN.ESPFM.csv','ALRW1N_SQIN.ESPF0.csv','ALRW1N_SQIN.ESPF10.csv','ALRW1N_SQIN.ESPFM.csv','AMFI1N_SQIN.ESPF0.csv','AMFI1N_SQIN.ESPF10.csv','AMFI1N_SQIN.ESPFM.csv','ANAW1N_SQIN.ESPF0.csv','ANAW1N_SQIN.ESPF10.csv','ANAW1N_SQIN.ESPFM.csv','ANTI1N_SQIN.ESPF0.csv','ANTI1N_SQIN.ESPF10.csv','ANTI1N_SQIN.ESPFM.csv','APLO3N_SQIN.ESPF0.csv','APLO3N_SQIN.ESPF10.csv','APLO3N_SQIN.ESPFM.csv','APRO3N_SQIN.ESPF0.csv','APRO3N_SQIN.ESPF10.csv','APRO3N_SQIN.ESPFM.csv','ARAI1N_SQIN.ESPF0.csv','ARAI1N_SQIN.ESPF10.csv','ARAI1N_SQIN.ESPFM.csv','ARDQ2IN_SQIN.ESPF0.csv','ARDQ2IN_SQIN.ESPF10.csv','ARDQ2IN_SQIN.ESPFM.csv','ARDW1N_SQIN.ESPF0.csv','ARDW1N_SQIN.ESPF10.csv','ARDW1N_SQIN.ESPFM.csv','ARGW1N_SQIN.ESPF0.csv','ARGW1N_SQIN.ESPF10.csv','ARGW1N_SQIN.ESPFM.csv','ARKI1N_SQIN.ESPF0.csv','ARKI1N_SQIN.ESPF10.csv','ARKI1N_SQIN.ESPFM.csv','ARLW1N_SQIN.ESPF0.csv','ARLW1N_SQIN.ESPF10.csv','ARLW1N_SQIN.ESPFM.csv','ARWO3N_SQIN.ESPF0.csv','ARWO3N_SQIN.ESPF10.csv','ARWO3N_SQIN.ESPFM.csv','ASCW1N_SQIN.ESPF0.csv','ASCW1N_SQIN.ESPF10.csv','ASCW1N_SQIN.ESPFM.csv','AUBW1N_SQIN.ESPF0.csv','AUBW1N_SQIN.ESPF10.csv','AUBW1N_SQIN.ESPFM.csv','AURO3N_SQIN.ESPF0.csv','AURO3N_SQIN.ESPF10.csv','AURO3N_SQIN.ESPFM.csv','AZAO3N_SQIN.ESPF0.csv','AZAO3N_SQIN.ESPF10.csv','AZAO3N_SQIN.ESPFM.csv','BCDW1N_SQIN.ESPF0.csv','BCDW1N_SQIN.ESPF10.csv','BCDW1N_SQIN.ESPFM.csv','BDDI1N_SQIN.ESPF0.csv','BDDI1N_SQIN.ESPF10.csv','BDDI1N_SQIN.ESPFM.csv','BEAO3N_SQIN.ESPF0.csv','BEAO3N_SQIN.ESPF10.csv','BEAO3N_SQIN.ESPFM.csv','BELM8N_SQIN.ESPF0.csv','BELM8N_SQIN.ESPF10.csv','BELM8N_SQIN.ESPFM.csv','BEUO3N_SQIN.ESPF0.csv','BEUO3N_SQIN.ESPF10.csv','BEUO3N_SQIN.ESPFM.csv','BFEI1N_SQIN.ESPF0.csv','BFEI1N_SQIN.ESPF10.csv','BFEI1N_SQIN.ESPFM.csv','BFKW4N_SQIN.ESPF0.csv','BFKW4N_SQIN.ESPF10.csv','BFKW4N_SQIN.ESPFM.csv','BFTI1N_SQIN.ESPF0.csv','BFTI1N_SQIN.ESPF10.csv','BFTI1N_SQIN.ESPFM.csv','BIGI1N_SQIN.ESPF0.csv','BIGI1N_SQIN.ESPF10.csv','BIGI1N_SQIN.ESPFM.csv','BIRQ2N_SQIN.ESPF0.csv','BIRQ2N_SQIN.ESPF10.csv','BIRQ2N_SQIN.ESPFM.csv','BITM8N_SQIN.ESPF0.csv','BITM8N_SQIN.ESPF10.csv','BITM8N_SQIN.ESPFM.csv','BLUO3N_SQIN.ESPF0.csv','BLUO3N_SQIN.ESPF10.csv','BLUO3N_SQIN.ESPFM.csv','BONM8N_SQIN.ESPF0.csv','BONM8N_SQIN.ESPF10.csv','BONM8N_SQIN.ESPFM.csv','BONO3N_SQIN.ESPF0.csv','BONO3N_SQIN.ESPF10.csv','BONO3N_SQIN.ESPFM.csv','BRDQ2N_SQIN.ESPF0.csv','BRDQ2N_SQIN.ESPF10.csv','BRDQ2N_SQIN.ESPFM.csv','BRFI1N_SQIN.ESPF0.csv','BRFI1N_SQIN.ESPF10.csv','BRFI1N_SQIN.ESPFM.csv','BRNI1N_SQIN.ESPF0.csv','BRNI1N_SQIN.ESPF10.csv','BRNI1N_SQIN.ESPFM.csv','BTSI1N_SQIN.ESPF0.csv','BTSI1N_SQIN.ESPF10.csv','BTSI1N_SQIN.ESPFM.csv','BULO3N_SQIN.ESPF0.csv','BULO3N_SQIN.ESPF10.csv','BULO3N_SQIN.ESPFM.csv','BUMW1N_SQIN.ESPF0.csv','BUMW1N_SQIN.ESPF10.csv','BUMW1N_SQIN.ESPFM.csv','BUSO3N_SQIN.ESPF0.csv','BUSO3N_SQIN.ESPF10.csv','BUSO3N_SQIN.ESPFM.csv','BWKI1N_SQIN.ESPF0.csv','BWKI1N_SQIN.ESPF10.csv','BWKI1N_SQIN.ESPFM.csv','CABI1N_SQIN.ESPF0.csv','CABI1N_SQIN.ESPF10.csv','CABI1N_SQIN.ESPFM.csv','CALW1N_SQIN.ESPF0.csv','CALW1N_SQIN.ESPF10.csv','CALW1N_SQIN.ESPFM.csv','CAMI1N_SQIN.ESPF0.csv','CAMI1N_SQIN.ESPF10.csv','CAMI1N_SQIN.ESPFM.csv','CANO3N_SQIN.ESPF0.csv','CANO3N_SQIN.ESPF10.csv','CANO3N_SQIN.ESPFM.csv','CASW1N_SQIN.ESPF0.csv','CASW1N_SQIN.ESPF10.csv','CASW1N_SQIN.ESPFM.csv','CENW1N_SQIN.ESPF0.csv','CENW1N_SQIN.ESPF10.csv','CENW1N_SQIN.ESPFM.csv','CFMM8N_SQIN.ESPF0.csv','CFMM8N_SQIN.ESPF10.csv','CFMM8N_SQIN.ESPFM.csv','CGMW1N_SQIN.ESPF0.csv','CGMW1N_SQIN.ESPF10.csv','CGMW1N_SQIN.ESPFM.csv','CGRO3N_SQIN.ESPF0.csv','CGRO3N_SQIN.ESPF10.csv','CGRO3N_SQIN.ESPFM.csv','CHDW1N_SQIN.ESPF0.csv','CHDW1N_SQIN.ESPF10.csv','CHDW1N_SQIN.ESPFM.csv','CHEI1N_SQIN.ESPF0.csv','CHEI1N_SQIN.ESPF10.csv','CHEI1N_SQIN.ESPFM.csv','CHJW1N_SQIN.ESPF0.csv','CHJW1N_SQIN.ESPF10.csv','CHJW1N_SQIN.ESPFM.csv','CHTO3N_SQIN.ESPF0.csv','CHTO3N_SQIN.ESPF10.csv','CHTO3N_SQIN.ESPFM.csv','CIYW1N_SQIN.ESPF0.csv','CIYW1N_SQIN.ESPF10.csv','CIYW1N_SQIN.ESPFM.csv','CLDI1N_SQIN.ESPF0.csv','CLDI1N_SQIN.ESPF10.csv','CLDI1N_SQIN.ESPFM.csv','CLEW1N_SQIN.ESPF0.csv','CLEW1N_SQIN.ESPF10.csv','CLEW1N_SQIN.ESPFM.csv','CLFW1N_SQIN.ESPF0.csv','CLFW1N_SQIN.ESPF10.csv','CLFW1N_SQIN.ESPFM.csv','COCO3N_SQIN.ESPF0.csv','COCO3N_SQIN.ESPF10.csv','COCO3N_SQIN.ESPFM.csv','COEI1N_SQIN.ESPF0.csv','COEI1N_SQIN.ESPF10.csv','COEI1N_SQIN.ESPFM.csv','COKW1N_SQIN.ESPF0.csv','COKW1N_SQIN.ESPF10.csv','COKW1N_SQIN.ESPFM.csv','CONW1N_SQIN.ESPF0.csv','CONW1N_SQIN.ESPF10.csv','CONW1N_SQIN.ESPFM.csv','CORO3N_SQIN.ESPF0.csv','CORO3N_SQIN.ESPF10.csv','CORO3N_SQIN.ESPFM.csv','COTO3N_SQIN.ESPF0.csv','COTO3N_SQIN.ESPF10.csv','COTO3N_SQIN.ESPFM.csv','CRNW1N_SQIN.ESPF0.csv','CRNW1N_SQIN.ESPF10.csv','CRNW1N_SQIN.ESPFM.csv','CRPW1N_SQIN.ESPF0.csv','CRPW1N_SQIN.ESPF10.csv','CRPW1N_SQIN.ESPFM.csv','CSCI1N_SQIN.ESPF0.csv','CSCI1N_SQIN.ESPF10.csv','CSCI1N_SQIN.ESPFM.csv','CTAW1N_SQIN.ESPF0.csv','CTAW1N_SQIN.ESPF10.csv','CTAW1N_SQIN.ESPFM.csv','CTLI1N_SQIN.ESPF0.csv','CTLI1N_SQIN.ESPF10.csv','CTLI1N_SQIN.ESPFM.csv','CWMO3N_SQIN.ESPF0.csv','CWMO3N_SQIN.ESPF10.csv','CWMO3N_SQIN.ESPFM.csv','DARM8N_SQIN.ESPF0.csv','DARM8N_SQIN.ESPF10.csv','DARM8N_SQIN.ESPFM.csv','DCDQ2N_SQIN.ESPF0.csv','DCDQ2N_SQIN.ESPF10.csv','DCDQ2N_SQIN.ESPFM.csv','DEEO3N_SQIN.ESPF0.csv','DEEO3N_SQIN.ESPF10.csv','DEEO3N_SQIN.ESPFM.csv','DETO3N_SQIN.ESPF0.csv','DETO3N_SQIN.ESPF10.csv','DETO3N_SQIN.ESPFM.csv','DGGI1N_SQIN.ESPF0.csv','DGGI1N_SQIN.ESPF10.csv','DGGI1N_SQIN.ESPFM.csv','DLGM8N_SQIN.ESPF0.csv','DLGM8N_SQIN.ESPF10.csv','DLGM8N_SQIN.ESPFM.csv','DLLO3N_SQIN.ESPF0.csv','DLLO3N_SQIN.ESPF10.csv','DLLO3N_SQIN.ESPFM.csv','DONO3N_SQIN.ESPF0.csv','DONO3N_SQIN.ESPF10.csv','DONO3N_SQIN.ESPFM.csv','DORO3N_SQIN.ESPF0.csv','DORO3N_SQIN.ESPF10.csv','DORO3N_SQIN.ESPFM.csv','DOTW1N_SQIN.ESPF0.csv','DOTW1N_SQIN.ESPF10.csv','DOTW1N_SQIN.ESPFM.csv','DRBI1N_SQIN.ESPF0.csv','DRBI1N_SQIN.ESPF10.csv','DRBI1N_SQIN.ESPFM.csv','DRMM8N_SQIN.ESPF0.csv','DRMM8N_SQIN.ESPF10.csv','DRMM8N_SQIN.ESPFM.csv','DRSW1N_SQIN.ESPF0.csv','DRSW1N_SQIN.ESPF10.csv','DRSW1N_SQIN.ESPFM.csv','DSRW1N_SQIN.ESPF0.csv','DSRW1N_SQIN.ESPF10.csv','DSRW1N_SQIN.ESPFM.csv','DWRI1N_SQIN.ESPF0.csv','DWRI1N_SQIN.ESPF10.csv','DWRI1N_SQIN.ESPFM.csv','EASI1N_SQIN.ESPF0.csv','EASI1N_SQIN.ESPF10.csv','EASI1N_SQIN.ESPFM.csv','EASW1N_SQIN.ESPF0.csv','EASW1N_SQIN.ESPF10.csv','EASW1N_SQIN.ESPFM.csv','ECDO3N_SQIN.ESPF0.csv','ECDO3N_SQIN.ESPF10.csv','ECDO3N_SQIN.ESPFM.csv','EGCO3N_SQIN.ESPF0.csv','EGCO3N_SQIN.ESPF10.csv','EGCO3N_SQIN.ESPFM.csv','EGLO3N_SQIN.ESPF0.csv','EGLO3N_SQIN.ESPF10.csv','EGLO3N_SQIN.ESPFM.csv','EKTO3N_SQIN.ESPF0.csv','EKTO3N_SQIN.ESPF10.csv','EKTO3N_SQIN.ESPFM.csv','ELKO3N_SQIN.ESPF0.csv','ELKO3N_SQIN.ESPF10.csv','ELKO3N_SQIN.ESPFM.csv','ELWW1N_SQIN.ESPF0.csv','ELWW1N_SQIN.ESPF10.csv','ELWW1N_SQIN.ESPFM.csv','EMMI1N_SQIN.ESPF0.csv','EMMI1N_SQIN.ESPF10.csv','EMMI1N_SQIN.ESPFM.csv','ENVI1N_SQIN.ESPF0.csv','ENVI1N_SQIN.ESPF10.csv','ENVI1N_SQIN.ESPFM.csv','ESTO3N_SQIN.ESPF0.csv','ESTO3N_SQIN.ESPF10.csv','ESTO3N_SQIN.ESPFM.csv','EUGO3N_SQIN.ESPF0.csv','EUGO3N_SQIN.ESPF10.csv','EUGO3N_SQIN.ESPFM.csv','FALO3N_SQIN.ESPF0.csv','FALO3N_SQIN.ESPF10.csv','FALO3N_SQIN.ESPFM.csv','FCFM8N_SQIN.ESPF0.csv','FCFM8N_SQIN.ESPF10.csv','FCFM8N_SQIN.ESPFM.csv','FFXW1N_SQIN.ESPF0.csv','FFXW1N_SQIN.ESPF10.csv','FFXW1N_SQIN.ESPFM.csv','FISM8N_SQIN.ESPF0.csv','FISM8N_SQIN.ESPF10.csv','FISM8N_SQIN.ESPFM.csv','FLGW4N_SQIN.ESPF0.csv','FLGW4N_SQIN.ESPF10.csv','FLGW4N_SQIN.ESPFM.csv','FOSO3N_SQIN.ESPF0.csv','FOSO3N_SQIN.ESPF10.csv','FOSO3N_SQIN.ESPFM.csv','FRMO3N_SQIN.ESPF0.csv','FRMO3N_SQIN.ESPF10.csv','FRMO3N_SQIN.ESPFM.csv','FRNO3N_SQIN.ESPF0.csv','FRNO3N_SQIN.ESPF10.csv','FRNO3N_SQIN.ESPFM.csv','FRYW1N_SQIN.ESPF0.csv','FRYW1N_SQIN.ESPF10.csv','FRYW1N_SQIN.ESPFM.csv','FSSO3N_SQIN.ESPF0.csv','FSSO3N_SQIN.ESPF10.csv','FSSO3N_SQIN.ESPFM.csv','GARW1N_SQIN.ESPF0.csv','GARW1N_SQIN.ESPF10.csv','GARW1N_SQIN.ESPFM.csv','GCDW1N_SQIN.ESPF0.csv','GCDW1N_SQIN.ESPF10.csv','GCDW1N_SQIN.ESPFM.csv','GFLW1N_SQIN.ESPF0.csv','GFLW1N_SQIN.ESPF10.csv','GFLW1N_SQIN.ESPFM.csv','GIBO3N_SQIN.ESPF0.csv','GIBO3N_SQIN.ESPF10.csv','GIBO3N_SQIN.ESPFM.csv','GLBW1N_SQIN.ESPF0.csv','GLBW1N_SQIN.ESPF10.csv','GLBW1N_SQIN.ESPFM.csv','GORW1N_SQIN.ESPF0.csv','GORW1N_SQIN.ESPF10.csv','GORW1N_SQIN.ESPFM.csv','GOSO3N_SQIN.ESPF0.csv','GOSO3N_SQIN.ESPF10.csv','GOSO3N_SQIN.ESPFM.csv','GPRO3N_SQIN.ESPF0.csv','GPRO3N_SQIN.ESPF10.csv','GPRO3N_SQIN.ESPFM.csv','GRAO3N_SQIN.ESPF0.csv','GRAO3N_SQIN.ESPF10.csv','GRAO3N_SQIN.ESPFM.csv','GREW4N_SQIN.ESPF0.csv','GREW4N_SQIN.ESPF10.csv','GREW4N_SQIN.ESPFM.csv','GVZW4N_SQIN.ESPF0.csv','GVZW4N_SQIN.ESPF10.csv','GVZW4N_SQIN.ESPFM.csv','HAGW1N_SQIN.ESPF0.csv','HAGW1N_SQIN.ESPF10.csv','HAGW1N_SQIN.ESPFM.csv','HALI1N_SQIN.ESPF0.csv','HALI1N_SQIN.ESPF10.csv','HALI1N_SQIN.ESPFM.csv','HARO3N_SQIN.ESPF0.csv','HARO3N_SQIN.ESPF10.csv','HARO3N_SQIN.ESPFM.csv','HCDI1N_SQIN.ESPF0.csv','HCDI1N_SQIN.ESPF10.csv','HCDI1N_SQIN.ESPFM.csv','HCRO3N_SQIN.ESPF0.csv','HCRO3N_SQIN.ESPF10.csv','HCRO3N_SQIN.ESPFM.csv','HEII1N_SQIN.ESPF0.csv','HEII1N_SQIN.ESPF10.csv','HEII1N_SQIN.ESPFM.csv','HHDW1N_SQIN.ESPF0.csv','HHDW1N_SQIN.ESPF10.csv','HHDW1N_SQIN.ESPFM.csv','HHWM8N_SQIN.ESPF0.csv','HHWM8N_SQIN.ESPF10.csv','HHWM8N_SQIN.ESPFM.csv','HLKW1N_SQIN.ESPF0.csv','HLKW1N_SQIN.ESPF10.csv','HLKW1N_SQIN.ESPFM.csv','HODO3N_SQIN.ESPF0.csv','HODO3N_SQIN.ESPF10.csv','HODO3N_SQIN.ESPFM.csv','HOPW1N_SQIN.ESPF0.csv','HOPW1N_SQIN.ESPF10.csv','HOPW1N_SQIN.ESPFM.csv','HOTI1N_SQIN.ESPF0.csv','HOTI1N_SQIN.ESPF10.csv','HOTI1N_SQIN.ESPFM.csv','HRSI1N_SQIN.ESPF0.csv','HRSI1N_SQIN.ESPF10.csv','HRSI1N_SQIN.ESPFM.csv','HWRI1N_SQIN.ESPF0.csv','HWRI1N_SQIN.ESPF10.csv','HWRI1N_SQIN.ESPFM.csv','IHDW1N_SQIN.ESPF0.csv','IHDW1N_SQIN.ESPF10.csv','IHDW1N_SQIN.ESPFM.csv','IMNO3N_SQIN.ESPF0.csv','IMNO3N_SQIN.ESPF10.csv','IMNO3N_SQIN.ESPFM.csv','ISLI1N_SQIN.ESPF0.csv','ISLI1N_SQIN.ESPF10.csv','ISLI1N_SQIN.ESPFM.csv','ISSW1N_SQIN.ESPF0.csv','ISSW1N_SQIN.ESPF10.csv','ISSW1N_SQIN.ESPFM.csv','JASO3N_SQIN.ESPF0.csv','JASO3N_SQIN.ESPF10.csv','JASO3N_SQIN.ESPFM.csv','JDAO3N_SQIN.ESPF0.csv','JDAO3N_SQIN.ESPF10.csv','JDAO3N_SQIN.ESPFM.csv','JFFO3N_SQIN.ESPF0.csv','JFFO3N_SQIN.ESPF10.csv','JFFO3N_SQIN.ESPFM.csv','JHNO3N_SQIN.ESPF0.csv','JHNO3N_SQIN.ESPF10.csv','JHNO3N_SQIN.ESPFM.csv','JKSW4N_SQIN.ESPF0.csv','JKSW4N_SQIN.ESPF10.csv','JKSW4N_SQIN.ESPFM.csv','JLKW4N_SQIN.ESPF0.csv','JLKW4N_SQIN.ESPF10.csv','JLKW4N_SQIN.ESPFM.csv','KACW1N_SQIN.ESPF0.csv','KACW1N_SQIN.ESPF10.csv','KACW1N_SQIN.ESPFM.csv','KEEW1N_SQIN.ESPF0.csv','KEEW1N_SQIN.ESPF10.csv','KEEW1N_SQIN.ESPFM.csv','KERM8IN_SQIN.ESPF0.csv','KERM8IN_SQIN.ESPF10.cs','KERM8IN_SQIN.ESPFM.csv','KIOW1N_SQIN.ESPF0.csv','KIOW1N_SQIN.ESPF10.csv','KIOW1N_SQIN.ESPFM.csv','KRBO3N_SQIN.ESPF0.csv','KRBO3N_SQIN.ESPF10.csv','KRBO3N_SQIN.ESPFM.csv','KTFW1N_SQIN.ESPF0.csv','KTFW1N_SQIN.ESPF10.csv','KTFW1N_SQIN.ESPFM.csv','LAUW1N_SQIN.ESPF0.csv','LAUW1N_SQIN.ESPF10.csv','LAUW1N_SQIN.ESPFM.csv','LEOI1N_SQIN.ESPF0.csv','LEOI1N_SQIN.ESPF10.csv','LEOI1N_SQIN.ESPFM.csv','LERI1N_SQIN.ESPF0.csv','LERI1N_SQIN.ESPF10.csv','LERI1N_SQIN.ESPFM.csv','LGDW1N_SQIN.ESPF0.csv','LGDW1N_SQIN.ESPF10.csv','LGDW1N_SQIN.ESPFM.csv','LGNO3N_SQIN.ESPF0.csv','LGNO3N_SQIN.ESPF10.csv','LGNO3N_SQIN.ESPFM.csv','LGSW1N_SQIN.ESPF0.csv','LGSW1N_SQIN.ESPF10.csv','LGSW1N_SQIN.ESPFM.csv','LLKW1N_SQIN.ESPF0.csv','LLKW1N_SQIN.ESPF10.csv','LLKW1N_SQIN.ESPFM.csv','LMNW1N_SQIN.ESPF0.csv','LMNW1N_SQIN.ESPF10.csv','LMNW1N_SQIN.ESPFM.csv','LNDW1N_SQIN.ESPF0.csv','LNDW1N_SQIN.ESPF10.csv','LNDW1N_SQIN.ESPFM.csv','LOCI1N_SQIN.ESPF0.csv','LOCI1N_SQIN.ESPF10.csv','LOCI1N_SQIN.ESPFM.csv','LOPO3N_SQIN.ESPF0.csv','LOPO3N_SQIN.ESPF10.csv','LOPO3N_SQIN.ESPFM.csv','LOSO3N_SQIN.ESPF0.csv','LOSO3N_SQIN.ESPF10.csv','LOSO3N_SQIN.ESPFM.csv','LSDW1N_SQIN.ESPF0.csv','LSDW1N_SQIN.ESPF10.csv','LSDW1N_SQIN.ESPFM.csv','LSMO3N_SQIN.ESPF0.csv','LSMO3N_SQIN.ESPF10.csv','LSMO3N_SQIN.ESPFM.csv','LSTO3N_SQIN.ESPF0.csv','LSTO3N_SQIN.ESPF10.csv','LSTO3N_SQIN.ESPFM.csv','LUCI1N_SQIN.ESPF0.csv','LUCI1N_SQIN.ESPF10.csv','LUCI1N_SQIN.ESPFM.csv','LYDM8N_SQIN.ESPF0.csv','LYDM8N_SQIN.ESPF10.csv','LYDM8N_SQIN.ESPFM.csv','MACI1N_SQIN.ESPF0.csv','MACI1N_SQIN.ESPF10.csv','MACI1N_SQIN.ESPFM.csv','MADO3N_SQIN.ESPF0.csv','MADO3N_SQIN.ESPF10.csv','MADO3N_SQIN.ESPFM.csv','MAGI1N_SQIN.ESPF0.csv','MAGI1N_SQIN.ESPF10.csv','MAGI1N_SQIN.ESPFM.csv','MCDQ2N_SQIN.ESPF0.csv','MCDQ2N_SQIN.ESPF10.csv','MCDQ2N_SQIN.ESPFM.csv','MCDW1N_SQIN.ESPF0.csv','MCDW1N_SQIN.ESPF10.csv','MCDW1N_SQIN.ESPFM.csv','MCKO3N_SQIN.ESPF0.csv','MCKO3N_SQIN.ESPF10.csv','MCKO3N_SQIN.ESPFM.csv','MCLO3N_SQIN.ESPF0.csv','MCLO3N_SQIN.ESPF10.csv','MCLO3N_SQIN.ESPFM.csv','MCMO3N_SQIN.ESPF0.csv','MCMO3N_SQIN.ESPF10.csv','MCMO3N_SQIN.ESPFM.csv','MCMW1N_SQIN.ESPF0.csv','MCMW1N_SQIN.ESPF10.csv','MCMW1N_SQIN.ESPFM.csv','MCZO3N_SQIN.ESPF0.csv','MCZO3N_SQIN.ESPF10.csv','MCZO3N_SQIN.ESPFM.csv','MEHO3N_SQIN.ESPF0.csv','MEHO3N_SQIN.ESPF10.csv','MEHO3N_SQIN.ESPFM.csv','MEWW1N_QINE.ESPF0.csv','MEWW1N_QINE.ESPF10.csv','MEWW1N_QINE.ESPFM.csv','MEWW1N_SQIN.ESPF0.csv','MEWW1N_SQIN.ESPF10.csv','MEWW1N_SQIN.ESPFM.csv','MFDO3N_SQIN.ESPF0.csv','MFDO3N_SQIN.ESPF10.csv','MFDO3N_SQIN.ESPFM.csv','MFNW1N_SQIN.ESPF0.csv','MFNW1N_SQIN.ESPF10.csv','MFNW1N_SQIN.ESPFM.csv','MFPI1N_SQIN.ESPF0.csv','MFPI1N_SQIN.ESPF10.csv','MFPI1N_SQIN.ESPFM.csv','MIDI1N_SQIN.ESPF0.csv','MIDI1N_SQIN.ESPF10.csv','MIDI1N_SQIN.ESPFM.csv','MILI1N_SQIN.ESPF0.csv','MILI1N_SQIN.ESPF10.csv','MILI1N_SQIN.ESPFM.csv','MKNW1N_SQIN.ESPF0.csv','MKNW1N_SQIN.ESPF10.csv','MKNW1N_SQIN.ESPFM.csv','MLBO3N_SQIN.ESPF0.csv','MLBO3N_SQIN.ESPF10.csv','MLBO3N_SQIN.ESPFM.csv','MLKW1N_SQIN.ESPF0.csv','MLKW1N_SQIN.ESPF10.csv','MLKW1N_SQIN.ESPFM.csv','MMRW1N_SQIN.ESPF0.csv','MMRW1N_SQIN.ESPF10.csv','MMRW1N_SQIN.ESPFM.csv','MNRO3N_SQIN.ESPF0.csv','MNRO3N_SQIN.ESPF10.csv','MNRO3N_SQIN.ESPFM.csv','MNSW1N_SQIN.ESPF0.csv','MNSW1N_SQIN.ESPF10.csv','MNSW1N_SQIN.ESPFM.csv','MODO3N_SQIN.ESPF0.csv','MODO3N_SQIN.ESPF10.csv','MODO3N_SQIN.ESPFM.csv','MONO3N_SQIN.ESPF0.csv','MONO3N_SQIN.ESPF10.csv','MONO3N_SQIN.ESPFM.csv','MORI1N_SQIN.ESPF0.csv','MORI1N_SQIN.ESPF10.csv','MORI1N_SQIN.ESPFM.csv','MORW1N_SQIN.ESPF0.csv','MORW1N_SQIN.ESPF10.csv','MORW1N_SQIN.ESPFM.csv','MPLO3N_SQIN.ESPF0.csv','MPLO3N_SQIN.ESPF10.csv','MPLO3N_SQIN.ESPFM.csv','MROW1N_SQIN.ESPF0.csv','MROW1N_SQIN.ESPF10.csv','MROW1N_SQIN.ESPFM.csv','MSRW1N_SQIN.ESPF0.csv','MSRW1N_SQIN.ESPF10.csv','MSRW1N_SQIN.ESPFM.csv','MVEW1N_SQIN.ESPF0.csv','MVEW1N_SQIN.ESPF10.csv','MVEW1N_SQIN.ESPFM.csv','MYDW1N_SQIN.ESPF0.csv','MYDW1N_SQIN.ESPF10.csv','MYDW1N_SQIN.ESPFM.csv','MYNO3N_SQIN.ESPF0.csv','MYNO3N_SQIN.ESPF10.csv','MYNO3N_SQIN.ESPFM.csv','MYPO3N_SQIN.ESPF0.csv','MYPO3N_SQIN.ESPF10.csv','MYPO3N_SQIN.ESPFM.csv','NACW1N_SQIN.ESPF0.csv','NACW1N_SQIN.ESPF10.csv','NACW1N_SQIN.ESPFM.csv','NASW1N_SQIN.ESPF0.csv','NASW1N_SQIN.ESPF10.csv','NASW1N_SQIN.ESPFM.csv','NEWW1N_SQIN.ESPF0.csv','NEWW1N_SQIN.ESPF10.csv','NEWW1N_SQIN.ESPFM.csv','NFFQ2N_SQIN.ESPF0.csv','NFFQ2N_SQIN.ESPF10.csv','NFFQ2N_SQIN.ESPFM.csv','NFNW1N_SQIN.ESPF0.csv','NFNW1N_SQIN.ESPF10.csv','NFNW1N_SQIN.ESPFM.csv','NISW1N_SQIN.ESPF0.csv','NISW1N_SQIN.ESPF10.csv','NISW1N_SQIN.ESPFM.csv','NITW1N_SQIN.ESPF0.csv','NITW1N_SQIN.ESPF10.csv','NITW1N_SQIN.ESPFM.csv','NKSW1N_SQIN.ESPF0.csv','NKSW1N_SQIN.ESPF10.csv','NKSW1N_SQIN.ESPFM.csv','NOXM8N_SQIN.ESPF0.csv','NOXM8N_SQIN.ESPF10.csv','NOXM8N_SQIN.ESPFM.csv','NRKW1N_SQIN.ESPF0.csv','NRKW1N_SQIN.ESPF10.csv','NRKW1N_SQIN.ESPFM.csv','NSPW1N_SQIN.ESPF0.csv','NSPW1N_SQIN.ESPF10.csv','NSPW1N_SQIN.ESPFM.csv','NSSW1N_SQIN.ESPF0.csv','NSSW1N_SQIN.ESPF10.csv','NSSW1N_SQIN.ESPFM.csv','OCHO3N_SQIN.ESPF0.csv','OCHO3N_SQIN.ESPF10.csv','OCHO3N_SQIN.ESPFM.csv','OCUO3N_SQIN.ESPF0.csv','OCUO3N_SQIN.ESPF10.csv','OCUO3N_SQIN.ESPFM.csv','OKMW1N_SQIN.ESPF0.csv','OKMW1N_SQIN.ESPF10.csv','OKMW1N_SQIN.ESPFM.csv','OKNW1N_SQIN.ESPF0.csv','OKNW1N_SQIN.ESPF10.csv','OKNW1N_SQIN.ESPFM.csv','ORFI1N_SQIN.ESPF0.csv','ORFI1N_SQIN.ESPF10.csv','ORFI1N_SQIN.ESPFM.csv','ORTW1N_SQIN.ESPF0.csv','ORTW1N_SQIN.ESPF10.csv','ORTW1N_SQIN.ESPFM.csv','OWYO3N_SQIN.ESPF0.csv','OWYO3N_SQIN.ESPF10.csv','OWYO3N_SQIN.ESPFM.csv','PACW1N_SQIN.ESPF0.csv','PACW1N_SQIN.ESPF10.csv','PACW1N_SQIN.ESPFM.csv','PACW4N_SQIN.ESPF0.csv','PACW4N_SQIN.ESPF10.csv','PACW4N_SQIN.ESPFM.csv','PALI1N_SQIN.ESPF0.csv','PALI1N_SQIN.ESPF10.csv','PALI1N_SQIN.ESPFM.csv','PARI1N_SQIN.ESPF0.csv','PARI1N_SQIN.ESPF10.csv','PARI1N_SQIN.ESPFM.csv','PARW1N_SQIN.ESPF0.csv','PARW1N_SQIN.ESPF10.csv','PARW1N_SQIN.ESPFM.csv','PATW1N_SQIN.ESPF0.csv','PATW1N_SQIN.ESPF10.csv','PATW1N_SQIN.ESPFM.csv','PDTO3N_SQIN.ESPF0.csv','PDTO3N_SQIN.ESPF10.csv','PDTO3N_SQIN.ESPFM.csv','PERM8N_SQIN.ESPF0.csv','PERM8N_SQIN.ESPF10.csv','PERM8N_SQIN.ESPFM.csv','PESW1N_SQIN.ESPF0.csv','PESW1N_SQIN.ESPF10.csv','PESW1N_SQIN.ESPFM.csv','PHIO3N_SQIN.ESPF0.csv','PHIO3N_SQIN.ESPF10.csv','PHIO3N_SQIN.ESPFM.csv','PHLO3N_SQIN.ESPF0.csv','PHLO3N_SQIN.ESPF10.csv','PHLO3N_SQIN.ESPFM.csv','PIHI1N_SQIN.ESPF0.csv','PIHI1N_SQIN.ESPF10.csv','PIHI1N_SQIN.ESPFM.csv','PILW1N_SQIN.ESPF0.csv','PILW1N_SQIN.ESPF10.csv','PILW1N_SQIN.ESPFM.csv','PITW1N_SQIN.ESPF0.csv','PITW1N_SQIN.ESPF10.csv','PITW1N_SQIN.ESPFM.csv','PLNM8N_SQIN.ESPF0.csv','PLNM8N_SQIN.ESPF10.csv','PLNM8N_SQIN.ESPFM.csv','PLOI1N_SQIN.ESPF0.csv','PLOI1N_SQIN.ESPF10.csv','PLOI1N_SQIN.ESPFM.csv','POWO3N_SQIN.ESPF0.csv','POWO3N_SQIN.ESPF10.csv','POWO3N_SQIN.ESPFM.csv','PRCI1N_SQIN.ESPF0.csv','PRCI1N_SQIN.ESPF10.csv','PRCI1N_SQIN.ESPFM.csv','PRCM8N_SQIN.ESPF0.csv','PRCM8N_SQIN.ESPF10.csv','PRCM8N_SQIN.ESPFM.csv','PRII1N_SQIN.ESPF0.csv','PRII1N_SQIN.ESPF10.csv','PRII1N_SQIN.ESPFM.csv','PRLI1N_SQIN.ESPF0.csv','PRLI1N_SQIN.ESPF10.csv','PRLI1N_SQIN.ESPFM.csv','PRPI1N_SQIN.ESPF0.csv','PRPI1N_SQIN.ESPF10.csv','PRPI1N_SQIN.ESPFM.csv','PRTI1N_SQIN.ESPF0.csv','PRTI1N_SQIN.ESPF10.csv','PRTI1N_SQIN.ESPFM.csv','PRTO3N_SQIN.ESPF0.csv','PRTO3N_SQIN.ESPF10.csv','PRTO3N_SQIN.ESPFM.csv','PRVO3N_SQIN.ESPF0.csv','PRVO3N_SQIN.ESPF10.csv','PRVO3N_SQIN.ESPFM.csv','PRWW1N_SQIN.ESPF0.csv','PRWW1N_SQIN.ESPF10.csv','PRWW1N_SQIN.ESPFM.csv','PULW1N_SQIN.ESPF0.csv','PULW1N_SQIN.ESPF10.csv','PULW1N_SQIN.ESPFM.csv','PUYW1N_SQIN.ESPF0.csv','PUYW1N_SQIN.ESPF10.csv','PUYW1N_SQIN.ESPFM.csv','PWDO3N_SQIN.ESPF0.csv','PWDO3N_SQIN.ESPF10.csv','PWDO3N_SQIN.ESPFM.csv','QBYQ2IN_SQIN.ESPF0.csv','QBYQ2IN_SQIN.ESPF10.csv','QBYQ2IN_SQIN.ESPFM.csv','RAWW1N_SQIN.ESPF0.csv','RAWW1N_SQIN.ESPF10.csv','RAWW1N_SQIN.ESPFM.csv','RCCM8N_SQIN.ESPF0.csv','RCCM8N_SQIN.ESPF10.csv','RCCM8N_SQIN.ESPFM.csv','RDLO3N_SQIN.ESPF0.csv','RDLO3N_SQIN.ESPF10.csv','RDLO3N_SQIN.ESPFM.csv','REVQ2N_SQIN.ESPF0.csv','REVQ2N_SQIN.ESPF10.csv','REVQ2N_SQIN.ESPFM.csv','REXI1N_SQIN.ESPF0.csv','REXI1N_SQIN.ESPF10.csv','REXI1N_SQIN.ESPFM.csv','RIGI1N_SQIN.ESPF0.csv','RIGI1N_SQIN.ESPF10.csv','RIGI1N_SQIN.ESPFM.csv','RIMW1N_SQIN.ESPF0.csv','RIMW1N_SQIN.ESPF10.csv','RIMW1N_SQIN.ESPFM.csv','RIRI1N_SQIN.ESPF0.csv','RIRI1N_SQIN.ESPF10.csv','RIRI1N_SQIN.ESPFM.csv','RISW1N_SQIN.ESPF0.csv','RISW1N_SQIN.ESPF10.csv','RISW1N_SQIN.ESPFM.csv','RNTW1N_SQIN.ESPF0.csv','RNTW1N_SQIN.ESPF10.csv','RNTW1N_SQIN.ESPFM.csv','RODW1N_SQIN.ESPF0.csv','RODW1N_SQIN.ESPF10.csv','RODW1N_SQIN.ESPFM.csv','RRHW1N_SQIN.ESPF0.csv','RRHW1N_SQIN.ESPF10.csv','RRHW1N_SQIN.ESPFM.csv','RSBO3N_SQIN.ESPF0.csv','RSBO3N_SQIN.ESPF10.csv','RSBO3N_SQIN.ESPFM.csv','RYGO3N_SQIN.ESPF0.csv','RYGO3N_SQIN.ESPF10.csv','RYGO3N_SQIN.ESPFM.csv','SAKW1N_SQIN.ESPF0.csv','SAKW1N_SQIN.ESPF10.csv','SAKW1N_SQIN.ESPFM.csv','SALW4N_SQIN.ESPF0.csv','SALW4N_SQIN.ESPF10.csv','SALW4N_SQIN.ESPFM.csv','SATI1N_SQIN.ESPF0.csv','SATI1N_SQIN.ESPF10.csv','SATI1N_SQIN.ESPFM.csv','SATW1N_SQIN.ESPF0.csv','SATW1N_SQIN.ESPF10.csv','SATW1N_SQIN.ESPFM.csv','SCOO3N_SQIN.ESPF0.csv','SCOO3N_SQIN.ESPF10.csv','SCOO3N_SQIN.ESPFM.csv','SCRO3N_SQIN.ESPF0.csv','SCRO3N_SQIN.ESPF10.csv','SCRO3N_SQIN.ESPFM.csv','SELI1N_SQIN.ESPF0.csv','SELI1N_SQIN.ESPF10.csv','SELI1N_SQIN.ESPFM.csv','SERO3N_SQIN.ESPF0.csv','SERO3N_SQIN.ESPF10.csv','SERO3N_SQIN.ESPFM.csv','SFLN2N_SQIN.ESPF0.csv','SFLN2N_SQIN.ESPF10.csv','SFLN2N_SQIN.ESPFM.csv','SHDW1N_SQIN.ESPF0.csv','SHDW1N_SQIN.ESPF10.csv','SHDW1N_SQIN.ESPFM.csv','SHYI1N_SQIN.ESPF0.csv','SHYI1N_SQIN.ESPF10.csv','SHYI1N_SQIN.ESPFM.csv','SIFI1N_SQIN.ESPF0.csv','SIFI1N_SQIN.ESPF10.csv','SIFI1N_SQIN.ESPFM.csv','SILO3N_SQIN.ESPF0.csv','SILO3N_SQIN.ESPF10.csv','SILO3N_SQIN.ESPFM.csv','SJMI1N_SSTG.ESPF0.csv','SJMI1N_SSTG.ESPF10.csv','SJMI1N_SSTG.ESPFM.csv','SKOW1N_SQIN.ESPF0.csv','SKOW1N_SQIN.ESPF10.csv','SKOW1N_SQIN.ESPFM.csv','SLCQ2N_SQIN.ESPF0.csv','SLCQ2N_SQIN.ESPF10.csv','SLCQ2N_SQIN.ESPFM.csv','SLKW1N_SQIN.ESPF0.csv','SLKW1N_SQIN.ESPF10.csv','SLKW1N_SQIN.ESPFM.csv','SLMO3N_SQIN.ESPF0.csv','SLMO3N_SQIN.ESPF10.csv','SLMO3N_SQIN.ESPFM.csv','SLTW1N_SQIN.ESPF0.csv','SLTW1N_SQIN.ESPF10.csv','SLTW1N_SQIN.ESPFM.csv','SMKQ2N_SQIN.ESPF0.csv','SMKQ2N_SQIN.ESPF10.csv','SMKQ2N_SQIN.ESPFM.csv','SMNI1N_SQIN.ESPF0.csv','SMNI1N_SQIN.ESPF10.csv','SMNI1N_SQIN.ESPFM.csv','SMRW1N_SQIN.ESPF0.csv','SMRW1N_SQIN.ESPF10.csv','SMRW1N_SQIN.ESPFM.csv','SNAI1N_SQIN.ESPF0.csv','SNAI1N_SQIN.ESPF10.csv','SNAI1N_SQIN.ESPFM.csv','SNDO3N_SQIN.ESPF0.csv','SNDO3N_SQIN.ESPF10.csv','SNDO3N_SQIN.ESPFM.csv','SNQW1N_SQIN.ESPF0.csv','SNQW1N_SQIN.ESPF10.csv','SNQW1N_SQIN.ESPFM.csv','SNYI1N_SQIN.ESPF0.csv','SNYI1N_SQIN.ESPF10.csv','SNYI1N_SQIN.ESPFM.csv','SPDI1N_SQIN.ESPF0.csv','SPDI1N_SQIN.ESPF10.csv','SPDI1N_SQIN.ESPFM.csv','SPEW1N_SQIN.ESPF0.csv','SPEW1N_SQIN.ESPF10.csv','SPEW1N_SQIN.ESPFM.csv','SPOW1N_SQIN.ESPF0.csv','SPOW1N_SQIN.ESPF10.csv','SPOW1N_SQIN.ESPFM.csv','SPRO3N_SQIN.ESPF0.csv','SPRO3N_SQIN.ESPF10.csv','SPRO3N_SQIN.ESPFM.csv','SQUW1N_SQIN.ESPF0.csv','SQUW1N_SQIN.ESPF10.csv','SQUW1N_SQIN.ESPFM.csv','SRGM8N_SQIN.ESPF0.csv','SRGM8N_SQIN.ESPF10.csv','SRGM8N_SQIN.ESPFM.csv','SRLM8N_SQIN.ESPF0.csv','SRLM8N_SQIN.ESPF10.csv','SRLM8N_SQIN.ESPFM.csv','SRMO3N_SQIN.ESPF0.csv','SRMO3N_SQIN.ESPF10.csv','SRMO3N_SQIN.ESPFM.csv','SRMW1N_SQIN.ESPF0.csv','SRMW1N_SQIN.ESPF10.csv','SRMW1N_SQIN.ESPFM.csv','SSUW1N_SQIN.ESPF0.csv','SSUW1N_SQIN.ESPF10.csv','SSUW1N_SQIN.ESPFM.csv','STHW1N_SQIN.ESPF0.csv','STHW1N_SQIN.ESPF10.csv','STHW1N_SQIN.ESPFM.csv','STII1N_SQIN.ESPF0.csv','STII1N_SQIN.ESPF10.csv','STII1N_SQIN.ESPFM.csv','STRM8N_SQIN.ESPF0.csv','STRM8N_SQIN.ESPF10.csv','STRM8N_SQIN.ESPFM.csv','SURO3N_SQIN.ESPF0.csv','SURO3N_SQIN.ESPF10.csv','SURO3N_SQIN.ESPFM.csv','SUVO3N_SQIN.ESPF0.csv','SUVO3N_SQIN.ESPF10.csv','SUVO3N_SQIN.ESPFM.csv','SWAI1N_SQIN.ESPF0.csv','SWAI1N_SQIN.ESPF10.csv','SWAI1N_SQIN.ESPFM.csv','SWRM8N_SQIN.ESPF0.csv','SWRM8N_SQIN.ESPF10.csv','SWRM8N_SQIN.ESPFM.csv','SYCO3N_SQIN.ESPF0.csv','SYCO3N_SQIN.ESPF10.csv','SYCO3N_SQIN.ESPFM.csv','TANW1N_SQIN.ESPF0.csv','TANW1N_SQIN.ESPF10.csv','TANW1N_SQIN.ESPFM.csv','TCHW1N_SQIN.ESPF0.csv','TCHW1N_SQIN.ESPF10.csv','TCHW1N_SQIN.ESPFM.csv','TDAO3N_SQIN.ESPF0.csv','TDAO3N_SQIN.ESPF10.csv','TDAO3N_SQIN.ESPFM.csv','TEAI1N_SQIN.ESPF0.csv','TEAI1N_SQIN.ESPF10.csv','TEAI1N_SQIN.ESPFM.csv','THNW1N_SQIN.ESPF0.csv','THNW1N_SQIN.ESPF10.csv','THNW1N_SQIN.ESPFM.csv','THRM8N_SQIN.ESPF0.csv','THRM8N_SQIN.ESPF10.csv','THRM8N_SQIN.ESPFM.csv','TIDO3N_SQIN.ESPF0.csv','TIDO3N_SQIN.ESPF10.csv','TIDO3N_SQIN.ESPFM.csv','TILO3N_SQIN.ESPF0.csv','TILO3N_SQIN.ESPF10.csv','TILO3N_SQIN.ESPFM.csv','TILW1N_SQIN.ESPF0.csv','TILW1N_SQIN.ESPF10.csv','TILW1N_SQIN.ESPFM.csv','TLMO3N_SQIN.ESPF0.csv','TLMO3N_SQIN.ESPF10.csv','TLMO3N_SQIN.ESPFM.csv','TLRW1N_SQIN.ESPF0.csv','TLRW1N_SQIN.ESPF10.csv','TLRW1N_SQIN.ESPFM.csv','TLYO3N_SQIN.ESPF0.csv','TLYO3N_SQIN.ESPF10.csv','TLYO3N_SQIN.ESPFM.csv','TNAW1N_SQIN.ESPF0.csv','TNAW1N_SQIN.ESPF10.csv','TNAW1N_SQIN.ESPFM.csv','TOLW1N_SQIN.ESPF0.csv','TOLW1N_SQIN.ESPF10.csv','TOLW1N_SQIN.ESPFM.csv','TONW1N_SQIN.ESPF0.csv','TONW1N_SQIN.ESPF10.csv','TONW1N_SQIN.ESPFM.csv','TOPI1N_SQIN.ESPF0.csv','TOPI1N_SQIN.ESPF10.csv','TOPI1N_SQIN.ESPFM.csv','TOTW1N_SQIN.ESPF0.csv','TOTW1N_SQIN.ESPF10.csv','TOTW1N_SQIN.ESPFM.csv','TRAO3N_SQIN.ESPF0.csv','TRAO3N_SQIN.ESPF10.csv','TRAO3N_SQIN.ESPFM.csv','TRBO3N_SQIN.ESPF0.csv','TRBO3N_SQIN.ESPF10.csv','TRBO3N_SQIN.ESPFM.csv','TRSO3N_SQIN.ESPF0.csv','TRSO3N_SQIN.ESPF10.csv','TRSO3N_SQIN.ESPFM.csv','TRYM8N_SQIN.ESPF0.csv','TRYM8N_SQIN.ESPF10.csv','TRYM8N_SQIN.ESPFM.csv','TRYO3N_SQIN.ESPF0.csv','TRYO3N_SQIN.ESPF10.csv','TRYO3N_SQIN.ESPFM.csv','UBDW1N_SQIN.ESPF0.csv','UBDW1N_SQIN.ESPF10.csv','UBDW1N_SQIN.ESPFM.csv','UMAO3N_SQIN.ESPF0.csv','UMAO3N_SQIN.ESPF10.csv','UMAO3N_SQIN.ESPFM.csv','UMTW1N_SQIN.ESPF0.csv','UMTW1N_SQIN.ESPF10.csv','UMTW1N_SQIN.ESPFM.csv','UNDW1N_SQIN.ESPF0.csv','UNDW1N_SQIN.ESPF10.csv','UNDW1N_SQIN.ESPFM.csv','UNYO3N_SQIN.ESPF0.csv','UNYO3N_SQIN.ESPF10.csv','UNYO3N_SQIN.ESPFM.csv','VALO3N_SQIN.ESPF0.csv','VALO3N_SQIN.ESPF10.csv','VALO3N_SQIN.ESPFM.csv','VICM8N_SQIN.ESPF0.csv','VICM8N_SQIN.ESPF10.csv','VICM8N_SQIN.ESPFM.csv','VIDO3N_SQIN.ESPF0.csv','VIDO3N_SQIN.ESPF10.csv','VIDO3N_SQIN.ESPFM.csv','WANQ2N_SQIN.ESPF0.csv','WANQ2N_SQIN.ESPF10.csv','WANQ2N_SQIN.ESPFM.csv','WANW1N_SQIN.ESPF0.csv','WANW1N_SQIN.ESPF10.csv','WANW1N_SQIN.ESPFM.csv','WARO3N_SQIN.ESPF0.csv','WARO3N_SQIN.ESPF10.csv','WARO3N_SQIN.ESPFM.csv','WCHW1N_SQIN.ESPF0.csv','WCHW1N_SQIN.ESPF10.csv','WCHW1N_SQIN.ESPFM.csv','WDHN2N_SQIN.ESPF0.csv','WDHN2N_SQIN.ESPF10.csv','WDHN2N_SQIN.ESPFM.csv','WEII1N_SQIN.ESPF0.csv','WEII1N_SQIN.ESPF10.csv','WEII1N_SQIN.ESPFM.csv','WELW1N_SQIN.ESPF0.csv','WELW1N_SQIN.ESPF10.csv','WELW1N_SQIN.ESPFM.csv','WFBM8N_SQIN.ESPF0.csv','WFBM8N_SQIN.ESPF10.csv','WFBM8N_SQIN.ESPFM.csv','WFRM8N_SQIN.ESPF0.csv','WFRM8N_SQIN.ESPF10.csv','WFRM8N_SQIN.ESPFM.csv','WGCM8N_SQIN.ESPF0.csv','WGCM8N_SQIN.ESPF10.csv','WGCM8N_SQIN.ESPFM.csv','WHBI1N_SQIN.ESPF0.csv','WHBI1N_SQIN.ESPF10.csv','WHBI1N_SQIN.ESPFM.csv','WHRM8N_SQIN.ESPF0.csv','WHRM8N_SQIN.ESPF10.csv','WHRM8N_SQIN.ESPFM.csv','WILW1N_SQIN.ESPF0.csv','WILW1N_SQIN.ESPF10.csv','WILW1N_SQIN.ESPFM.csv','WLAO3N_SQIN.ESPF0.csv','WLAO3N_SQIN.ESPF10.csv','WLAO3N_SQIN.ESPFM.csv','WLSO3N_SQIN.ESPF0.csv','WLSO3N_SQIN.ESPF10.csv','WLSO3N_SQIN.ESPFM.csv','WNRO3N_SQIN.ESPF0.csv','WNRO3N_SQIN.ESPF10.csv','WNRO3N_SQIN.ESPFM.csv','WRAW1N_SQIN.ESPF0.csv','WRAW1N_SQIN.ESPF10.csv','WRAW1N_SQIN.ESPFM.csv','WSLO3N_SQIN.ESPF0.csv','WSLO3N_SQIN.ESPF10.csv','WSLO3N_SQIN.ESPFM.csv','WSNO3N_SQIN.ESPF0.csv','WSNO3N_SQIN.ESPF10.csv','WSNO3N_SQIN.ESPFM.csv','WSRI1N_SQIN.ESPF0.csv','WSRI1N_SQIN.ESPF10.csv','WSRI1N_SQIN.ESPFM.csv','WTHW1N_SQIN.ESPF0.csv','WTHW1N_SQIN.ESPF10.csv','WTHW1N_SQIN.ESPFM.csv','WTLO3N_SQIN.ESPF0.csv','WTLO3N_SQIN.ESPF10.csv','WTLO3N_SQIN.ESPFM.csv','WYDW1N_SQIN.ESPF0.csv','WYDW1N_SQIN.ESPF10.csv','WYDW1N_SQIN.ESPFM.csv"
]

TenDayESP = []
FiveDayESP = []
ZeroDayESP = []
MiscDays = []
EspDaysCSV = []
FileNames = []

for n in range(len(CSV_List_Options_NorthWestRFC)):
	CsvEndName = CSV_List_Options_NorthWestRFC[n]
	#need to change x to a variable name that makes sense once I know what that would be.
	if CsvEndName[-6:]=="10.csv":
		TenDayESP.append(CsvEndName)
	elif CsvEndName[-5:] == "0.csv":
		ZeroDayESP.append(CsvEndName)
	elif CsvEndName[-5:] == "5.csv":
		FiveDayESP.append(CsvEndName) 
	else:
		MiscDays.append(CsvEndName)
		

if EspDays =="0":
	EspDaysCSV = ZeroDayESP
elif EspDays =="5":
	EspDaysCSV = FiveDayESP
elif EspDays =="10":
	EspDaysCSV = TenDayESP

for i in range(len(GoI_NoSpace)):
	NorthWestRFT_URL = "https://www.nwrfc.noaa.gov/chpsesp/ensemble/natural/"

	GagesUsed = []
	GagesToDownload(EspDaysCSV)

	#CheckOnSpelling(GagesUsed)
	#Want to use a function to throw an exception if the infroamtion the user inputted is not within the list.
	#This is not working at this time, so if the user does not type the location in like denoted in the list, an error in the script will occur
	# and is only visible in the console. This error is not the best if the user does not understand how the code is working and parsing the data.
	
	ESP_TraceOfInterest = GagesUsed[i]
	webrequest = NorthWestRFT_URL+GagesUsed[i]
	
	#Temp Download process
	FileLocation =SaveLocation.rsplit('\\',1)[0]
	FileName = GagesUsed[i]
	FileNames.append(FileName)
	downloadFile(webrequest,FileLocation+"\\"+FileName)
	
	#Function to do converstions
	
	#Data manipulation 
	data = readCSV(FileLocation+"\\"+FileName)
	SaveToDSS(data,SaveLocation, EspDays, webrequest)
#This has an addition of webrequest as an input to th e the "SaveToDSS" function call.

print("-"*100)
print("Defined Parameters")
print("DSS File Location: %s" %SaveLocation)
print("ESP Days: %s" %EspDays)
print("File Location: %s" %FileLocation)
print("File Names: %s" %FileNames)
print("-"*100)

JOptionPane.showMessageDialog(None , "The script has finished collecting the data and placed into the designated dss file.")
