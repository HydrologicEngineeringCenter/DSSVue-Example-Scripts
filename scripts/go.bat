cd %~dp0
set J=C:\Programs\CWMS-v3.2.1.256\common\exe\runhere.exe
rem run program  
::call %J% jython %1 %2  


rem redirect output to a file, then copy file to screen.
call %J% jython %1 %2  > tmp{010}.txt 2>&1
type tmp{010}.txt
echo done running %1


::start "title" /WAIT /B C:\Programs\CWMS-v3.2.1.256\common\exe\runhere.exe jython VsCode-sample.py .

:: uses existing vscode window  
::start "jython %1" /WAIT /B %J% jython %1 %2 

:: new window but closes when done..
::start "jython %1" /WAIT %J% jython %1 %2  

