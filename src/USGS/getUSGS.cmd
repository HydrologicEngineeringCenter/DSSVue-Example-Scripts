set JAVA_HOME C:\Programs\CWMS-v3.2.1\shared\java64
set path=C:\Programs\CWMS-v3.2.1\shared\java64\bin;%path%

C:
cd "C:\Programs\CWMS-v3.2.1\common\exe"
set GS=C:\Programs\getUSGS
set GS=C:\project\DSSVue-Example-Scripts\src\USGS

::call jython %GS%\getusgs.py -w %GS% -l SAS.csv -p parameters.csv -a parameter_aliases.csv  -h 24 -o VERBOSE  -d my.dss
call jython %GS%\getusgs_293.py -w %GS% -l SAS.csv -p parameters.csv -a parameter_aliases.csv  -h 24 -o VERBOSE  -d my.dss

pause