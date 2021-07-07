# name=ESP Data Importer CNRFC
# displayinmenu=true
# displaytouser=true
# displayinselector=true
from  javax.swing		import JOptionPane
from  java.util		import ArrayList
from hec.heclib.dss	import HecDss
from hec.heclib.util 	import HecTime
from hec.hecmath		import TimeSeriesMath
from hec.io			import TimeSeriesContainer
from hec.script		import Constants
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
	tsc.values = [Constants.UNDEFINED]*len(times) #add null data number here.
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
	
def SaveToDSS(rawDataList,SaveLocation,URLSite):
	 #From raw data list, saves the list of ESP dataframes to file
	#  If saveLocation is a file, saves there.  saveLocation can also
	#  be a directory, in which case a default file name is written provided
	#  the espDays  argument is assigned	
	if SaveLocation[-3:].upper()=='DSS':
		outFileName =  ("%s" %(SaveLocation))
	else:
		outFileName = ("%s\\rfc_esp_flows.dss" % (SaveLocation))
	dssFile = HecDss.open(outFileName,1)

	ESP_Matrix = rawDataList[2:] #This is set for NW RFC's data. There is extra meta data that we do not need to parse through

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
	#SaveLocation = JOptionPane.showInputDialog( "Please input a save location (Do not end with '\\')'.\nYou can either put in a DSS file location to specify a name or a file location and a default name will be popualted")
	SaveLocation = "C:\Users\q0hecajd\Desktop\Temp\Scripts\TestData.dss"
elif DssFileLocation == "Same as Open DSS File":
	None
	#Want this to be able to automatically direct to the open DSS file. 
#GagesOfInterest = JOptionPane.showInputDialog( "Please input the gage identifiers (seperate with a common for multiple locations")
GagesOfInterest = "MARN2, FTDC1, BTYO3, CHSO3,WMSO3"

GagesOfInterest = GagesOfInterest .rsplit(',')

GoI_NoSpace = []
for i in range(len(GagesOfInterest)):
		GoI_NoSpace.append(GagesOfInterest[i].replace( " ",""))
'''
EspDaysChoices = ( "0", "10" )
#EspDays = JOptionPane.showInputDialog(None, "How many Days of the short-term weather forecast?","ESP Days", JOptionPane.QUESTION_MESSAGE, None,  EspDaysChoices, EspDaysChoices[0])
EspDays = "0"
'''
#ESP Days is not an option for CNRFC. All the data is the same for options.

print("\n\nBeginning ESP Download\n")

CSV_List_Options_CaliforniaNevadaRFC = [
'ADOC1_hefs_csv_hourly.csv','AHOC1_hefs_csv_hourly.csv','AKYC1_hefs_csv_hourly.csv','ALRC1_hefs_csv_hourly.csv','ANDC1_hefs_csv_hourly.csv','ANOC1_hefs_csv_hourly.csv','ANTC1_hefs_csv_hourly.csv','APCC1_hefs_csv_hourly.csv','ARCC1_hefs_csv_hourly.csv','AROC1_hefs_csv_hourly.csv','AVYC1_hefs_csv_hourly.csv','BCAC1_hefs_csv_hourly.csv','BCKC1_hefs_csv_hourly.csv','BDBC1_hefs_csv_hourly.csv','BHNC1_hefs_csv_hourly.csv','BKCC1_hefs_csv_hourly.csv','BLBC1_hefs_csv_hourly.csv','BNCC1_hefs_csv_hourly.csv','BOYO3_hefs_csv_hourly.csv','BPRC1_hefs_csv_hourly.csv','BRGC1_hefs_csv_hourly.csv','BSCC1_hefs_csv_hourly.csv','BSRC1_hefs_csv_hourly.csv','BTCC1_hefs_csv_hourly.csv','BTYO3_hefs_csv_hourly.csv','BURC1_hefs_csv_hourly.csv','BWKC1_hefs_csv_hourly.csv','CADC1_hefs_csv_hourly.csv','CBAC1_hefs_csv_hourly.csv','CCHC1_hefs_csv_hourly.csv','CDLC1_hefs_csv_hourly.csv','CEGC1_hefs_csv_hourly.csv','CEMC1_hefs_csv_hourly.csv','CFWC1_hefs_csv_hourly.csv','CHSO3_hefs_csv_hourly.csv','CHVC1_hefs_csv_hourly.csv','CKEC1_hefs_csv_hourly.csv','CLAC1_hefs_csv_hourly.csv','CLKC1_hefs_csv_hourly.csv','CLLC1_hefs_csv_hourly.csv','CLSC1_hefs_csv_hourly.csv','CLUC1_hefs_csv_hourly.csv','CMIC1_hefs_csv_hourly.csv','CMPC1_hefs_csv_hourly.csv','CMSN2_hefs_csv_hourly.csv','CNBC1_hefs_csv_hourly.csv','COTC1_hefs_csv_hourly.csv','COYC1_hefs_csv_hourly.csv','CREC1_hefs_csv_hourly.csv','CSKC1_hefs_csv_hourly.csv','CTIC1_hefs_csv_hourly.csv','CVQC1_hefs_csv_hourly.csv','CWAC1_hefs_csv_hourly.csv','CWCC1_hefs_csv_hourly.csv','CYBC1_hefs_csv_hourly.csv','DCMC1_hefs_csv_hourly.csv','DCSC1_hefs_csv_hourly.csv','DCVC1_hefs_csv_hourly.csv','DIXN2_hefs_csv_hourly.csv','DKHC1_hefs_csv_hourly.csv','DLMC1_hefs_csv_hourly.csv','DLTC1_hefs_csv_hourly.csv','DMCC1_hefs_csv_hourly.csv','DNRC1_hefs_csv_hourly.csv','DOSC1_hefs_csv_hourly.csv','DSNC1_hefs_csv_hourly.csv','DVGN2_hefs_csv_hourly.csv','DVSC1_hefs_csv_hourly.csv','EDCC1_hefs_csv_hourly.csv','EDOC1_hefs_csv_hourly.csv','EFBC1_hefs_csv_hourly.csv','ELPC1_hefs_csv_hourly.csv','EPRC1_hefs_csv_hourly.csv','EXQC1_hefs_csv_hourly.csv','FARC1_hefs_csv_hourly.csv','FHDC1_hefs_csv_hourly.csv','FMDC1_hefs_csv_hourly.csv','FMWC1_hefs_csv_hourly.csv','FOCC1_hefs_csv_hourly.csv','FOLC1_hefs_csv_hourly.csv','FRAC1_hefs_csv_hourly.csv','FRGC1_hefs_csv_hourly.csv','FRNC1_hefs_csv_hourly.csv','FSNC1_hefs_csv_hourly.csv','FTCN2_hefs_csv_hourly.csv','FTDC1_hefs_csv_hourly.csv','FTJC1_hefs_csv_hourly.csv','FTSC1_hefs_csv_hourly.csv','GARC1_hefs_csv_hourly.csv','GERO3_hefs_csv_hourly.csv','GEYC1_hefs_csv_hourly.csv','GRDN2_hefs_csv_hourly.csv','GUAC1_hefs_csv_hourly.csv','GUDC1_hefs_csv_hourly.csv','GUEC1_hefs_csv_hourly.csv','GYRC1_hefs_csv_hourly.csv','HAMC1_hefs_csv_hourly.csv','HAPC1_hefs_csv_hourly.csv','HAWC1_hefs_csv_hourly.csv','HBMN2_hefs_csv_hourly.csv','HCHC1_hefs_csv_hourly.csv','HEAC1_hefs_csv_hourly.csv','HETC1_hefs_csv_hourly.csv','HIDC1_hefs_csv_hourly.csv','HKCC1_hefs_csv_hourly.csv','HLEC1_hefs_csv_hourly.csv','HLLC1_hefs_csv_hourly.csv','HOOC1_hefs_csv_hourly.csv','HOPC1_hefs_csv_hourly.csv','HOSC1_hefs_csv_hourly.csv','HOUC1_hefs_csv_hourly.csv','HPIC1_hefs_csv_hourly.csv','HRCN2_hefs_csv_hourly.csv','HREN2_hefs_csv_hourly.csv','HRIN2_hefs_csv_hourly.csv','HSAC1_hefs_csv_hourly.csv','HYMC1_hefs_csv_hourly.csv','ICHC1_hefs_csv_hourly.csv','IIFC1_hefs_csv_hourly.csv','ILAC1_hefs_csv_hourly.csv','INVC1_hefs_csv_hourly.csv','IRGC1_hefs_csv_hourly.csv','ISAC1_hefs_csv_hourly.csv','JKRC1_hefs_csv_hourly.csv','JNSC1_hefs_csv_hourly.csv','KCVC1_hefs_csv_hourly.csv','KEOO3_hefs_csv_hourly.csv','KKVC1_hefs_csv_hourly.csv','KLAO3_hefs_csv_hourly.csv','KNBC1_hefs_csv_hourly.csv','KTRC1_hefs_csv_hourly.csv','LAMC1_hefs_csv_hourly.csv','LBDC1_hefs_csv_hourly.csv','LBEC1_hefs_csv_hourly.csv','LEGC1_hefs_csv_hourly.csv','LEXC1_hefs_csv_hourly.csv','LLYC1_hefs_csv_hourly.csv','LNRC1_hefs_csv_hourly.csv','LSEC1_hefs_csv_hourly.csv','LTDC1_hefs_csv_hourly.csv','LVKC1_hefs_csv_hourly.csv','LWDC1_hefs_csv_hourly.csv','LWON2_hefs_csv_hourly.csv','MARN2_hefs_csv_hourly.csv','MEEC1_hefs_csv_hourly.csv','MFAC1_hefs_csv_hourly.csv','MFPC1_hefs_csv_hourly.csv','MFTC1_hefs_csv_hourly.csv','MHBC1_hefs_csv_hourly.csv','MHSN2_hefs_csv_hourly.csv','MLIC0_hefs_csv_hourly.csv','MLMC1_hefs_csv_hourly.csv','MLPC1_hefs_csv_hourly.csv','MPAC1_hefs_csv_hourly.csv','MPTC1_hefs_csv_hourly.csv','MRMC1_hefs_csv_hourly.csv','MRNC1_hefs_csv_hourly.csv','MSGC1_hefs_csv_hourly.csv','MSSC1_hefs_csv_hourly.csv','MTSC1_hefs_csv_hourly.csv','MUPC1_hefs_csv_hourly.csv','MUTC1_hefs_csv_hourly.csv','MVDC1_hefs_csv_hourly.csv','MVVC1_hefs_csv_hourly.csv','MWEC1_hefs_csv_hourly.csv','MWXC1_hefs_csv_hourly.csv','NACC1_hefs_csv_hourly.csv','NBBC1_hefs_csv_hourly.csv','NBYC1_hefs_csv_hourly.csv','NDPC1_hefs_csv_hourly.csv','NDVC1_hefs_csv_hourly.csv','NFDC1_hefs_csv_hourly.csv','NFEC1_hefs_csv_hourly.csv','NHGC1_hefs_csv_hourly.csv','NMFC1_hefs_csv_hourly.csv','NMSC1_hefs_csv_hourly.csv','NSWC1_hefs_csv_hourly.csv','NVRC1_hefs_csv_hourly.csv','ONSC1_hefs_csv_hourly.csv','ORDC1_hefs_csv_hourly.csv','ORFC1_hefs_csv_hourly.csv','ORIC1_hefs_csv_hourly.csv','OURC1_hefs_csv_hourly.csv','OWCC1_hefs_csv_hourly.csv','PALN2_hefs_csv_hourly.csv','PCGC1_hefs_csv_hourly.csv','PFTC1_hefs_csv_hourly.csv','PIIC1_hefs_csv_hourly.csv','PITC1_hefs_csv_hourly.csv','PLBC1_hefs_csv_hourly.csv','PLLC1_hefs_csv_hourly.csv','PLYC1_hefs_csv_hourly.csv','POHC1_hefs_csv_hourly.csv','PRBC1_hefs_csv_hourly.csv','PSRC1_hefs_csv_hourly.csv','PYMC1_hefs_csv_hourly.csv','RBBC1_hefs_csv_hourly.csv','RDBC1_hefs_csv_hourly.csv','RDRC1_hefs_csv_hourly.csv','RMKC1_hefs_csv_hourly.csv','ROCN2_hefs_csv_hourly.csv','ROLC1_hefs_csv_hourly.csv','SACC0_hefs_csv_hourly.csv','SACC1_hefs_csv_hourly.csv','SAMC1_hefs_csv_hourly.csv','SBRC1_hefs_csv_hourly.csv','SCBC1_hefs_csv_hourly.csv','SCNO3_hefs_csv_hourly.csv','SCOC1_hefs_csv_hourly.csv','SCPC1_hefs_csv_hourly.csv','SCRN2_hefs_csv_hourly.csv','SCSC1_hefs_csv_hourly.csv','SCWN2_hefs_csv_hourly.csv','SEIC1_hefs_csv_hourly.csv','SESC1_hefs_csv_hourly.csv','SFCC1_hefs_csv_hourly.csv','SGEC1_hefs_csv_hourly.csv','SGNC1_hefs_csv_hourly.csv','SHDC1_hefs_csv_hourly.csv','SHEC1_hefs_csv_hourly.csv','SHRC1_hefs_csv_hourly.csv','SKPC1_hefs_csv_hourly.csv','SKRC1_hefs_csv_hourly.csv','SLOC1_hefs_csv_hourly.csv','SLUC1_hefs_csv_hourly.csv','SMHC1_hefs_csv_hourly.csv','SNRC1_hefs_csv_hourly.csv','SOSC1_hefs_csv_hourly.csv','SOVC1_hefs_csv_hourly.csv','SREC1_hefs_csv_hourly.csv','SRWC1_hefs_csv_hourly.csv','SSAC1_hefs_csv_hourly.csv','SSQC1_hefs_csv_hourly.csv','STPC1_hefs_csv_hourly.csv','STWN2_hefs_csv_hourly.csv','SUAC1_hefs_csv_hourly.csv','SUSC1_hefs_csv_hourly.csv','SVCC1_hefs_csv_hourly.csv','SVIC1_hefs_csv_hourly.csv','SVWC1_hefs_csv_hourly.csv','TAHC1_hefs_csv_hourly.csv','TCCC1_hefs_csv_hourly.csv','TCRC1_hefs_csv_hourly.csv','TEHC1_hefs_csv_hourly.csv','TEKC1_hefs_csv_hourly.csv','THLC1_hefs_csv_hourly.csv','TIMC1_hefs_csv_hourly.csv','TISC1_hefs_csv_hourly.csv','TMDC1_hefs_csv_hourly.csv','TRCC1_hefs_csv_hourly.csv','TRRN2_hefs_csv_hourly.csv','TSLC1_hefs_csv_hourly.csv','TVRC1_hefs_csv_hourly.csv','TWDC1_hefs_csv_hourly.csv','UKAC1_hefs_csv_hourly.csv','UNVC1_hefs_csv_hourly.csv','VCAC1_hefs_csv_hourly.csv','VISN2_hefs_csv_hourly.csv','VLKC1_hefs_csv_hourly.csv','VNSC0_hefs_csv_hourly.csv','VONC1_hefs_csv_hourly.csv','VRVC1_hefs_csv_hourly.csv','VWBC1_hefs_csv_hourly.csv','WBGC1_hefs_csv_hourly.csv','WFMC1_hefs_csv_hourly.csv','WHSC1_hefs_csv_hourly.csv','WKAO3_hefs_csv_hourly.csv','WLKC1_hefs_csv_hourly.csv','WMSO3_hefs_csv_hourly.csv','WOOC1_hefs_csv_hourly.csv','WSDC1_hefs_csv_hourly.csv','WWBC1_hefs_csv_hourly.csv','YDRC1_hefs_csv_hourly.csv','YREC1_hefs_csv_hourly.csv','YTLC1_hefs_csv_hourly.csv'
]

#instead of this list, can I construct the URL around the site ID and just hope it is correct?
#URL_Generator = "https://www.cnrfc.noaa.gov/csv/%s_hefs_csv_hourly.csv" %GoI_NoSpace
#Would something like this work???

TenDayESP = []
FiveDayESP = []
ZeroDayESP = []
MiscDays = []
EspDaysCSV = []
FileNames = []
'''
for n in range(len(CSV_List_Options_CaliforniaNevadaRFC)):
	CsvEndName = CSV_List_Options_CaliforniaNevadaRFC[n]
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
'''

for i in range(len(GoI_NoSpace)):
	CaliforniaNevadaRFC_URL = "https://www.cnrfc.noaa.gov/csv/"

	GagesUsed = []
	GagesToDownload(CSV_List_Options_CaliforniaNevadaRFC)

	#CheckOnSpelling(GagesUsed)
	#Want to use a function to throw an exception if the infroamtion the user inputted is not within the list.
	#This is not working at this time, so if the user does not type the location in like denoted in the list, an error in the script will occur
	# and is only visible in the console. This error is not the best if the user does not understand how the code is working and parsing the data.
	
	ESP_TraceOfInterest = GagesUsed[i].rsplit('_',3)[0]
	webrequest = CaliforniaNevadaRFC_URL+GagesUsed[i]
	
	#Temp Download process
	FileLocation =SaveLocation.rsplit('\\',1)[0]
	FileName = GagesUsed[i]
	FileNames.append(FileName)
	downloadFile(webrequest,FileLocation+"\\"+FileName)
	
	#Function to do converstions
	
	#Data manipulation 
	data = readCSV(FileLocation+"\\"+FileName)
	SaveToDSS(data,SaveLocation, webrequest)
#This has an addition of webrequest as an input to th e the "SaveToDSS" function call.

print("-"*100)
print("Defined Parameters")
print("DSS File Location: %s" %SaveLocation)
#print("ESP Days: %s" %EspDays)
print("File Location: %s" %FileLocation)
print("File Names: %s" %FileNames)
print("-"*100)

#JOptionPane.showMessageDialog(None , "The script has finished collecting the data and placed into the designated dss file.")
