set J=C:\Programs\CWMS-v3.2.1.256\common\exe\runhere.exe
cd  %~dp0
copy data\sample.dss  c:\temp\
for /r %%f in (src\*.py) do start %J% jython src\%%~nxf 
pause