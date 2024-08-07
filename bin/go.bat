cd %~dp0
set J=C:\Users\Administrator\Desktop\CWMS-v3.2.1.459b\common\exe\runhere.exe Jython
rem run program  


rem redirect output to a file, then copy file to screen.
call %J% %1 %2 %3  
echo %ERRORLEVEL%
echo done running %1

