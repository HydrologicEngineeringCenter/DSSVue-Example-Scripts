set J=C:\Programs\CWMS-v3.2.1.256\common\exe\runhere.exe
cd  %~dp0

@echo off
for /r %%v in (*.py) do %J% jython "%%v" 

pause
