set J=C:\Programs\CWMS-v3.2.1.256\common\exe\runhere.exe
call %J% jython %1 %2

echo done running %1
::start "title" /WAIT /B C:\Programs\CWMS-v3.2.1.256\common\exe\runhere.exe jython VsCode-sample.py .

:: uses existing cscode window  
::start "jython %1" /WAIT /B %J% jython %1 %2 


:: new window but closes when done..
::start "jython %1" /WAIT %J% jython %1 %2


