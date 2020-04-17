set J=C:\Programs\CWMS-v3.2.1.256\common\exe\runhere.exe
cd  %~dp0
copy data\sample.dss  c:\temp\
@echo off
for /r %%v in (src\*.py) do %J% jython src\"%%v" 

pause
