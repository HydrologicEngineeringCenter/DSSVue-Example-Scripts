# Acessing the DSS API from system Jython
To acess the DSS API from a system jython requires you to configure your system environment. You need to create the environment using a combination of system environment variables and setting the java library for jython.

## Jython system variables
Several paths need to be appended to `sys.path`.

```python
import sys
sys.path.append(r"C:\local_software\HEC-DSSVue-v4.0.00.345\jar\sys\jythonUtils.jar")
sys.path.append(r"C:\local_software\HEC-DSSVue-v4.0.00.345\jar\hec.jar")
sys.path.append(r"C:\local_software\HEC-DSSVue-v4.0.00.345\jar\jython-standalone-2.7.0.jar")
sys.path.append(r"C:\local_software\HEC-DSSVue-v4.0.00.345\jar\hec-dssvue-dev.jar")
sys.path.append(r"C:\local_software\HEC-DSSVue-v4.0.00.345\jar\rma.jar")
```
## Set the java library for jython
This is acheived using the `-Djava.library.path=` arguement for the jython executable.

```cmd
C:\jython2.7.2\bin\jython.exe -Djava.library.path=C:\local_software\HEC-DSSVue-v4.0.00.345\lib
```
