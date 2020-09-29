cd %~dp0
set J=C:\Users\Administrator\Desktop\CWMS-v3.2.1.459b\common\exe\HEC-DSSVue.exe
rem run directly with Jython  


rem redirect output to a file, then copy file to screen.
call %J% %1
echo done running DSSVue tests