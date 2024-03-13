Example Usage:


C:\project\DSSVue-Example-Scripts\src\grids>c:\bin\HEC-DSSVue-3.4.0-RC02\jython.bat %CD%\esri_ascii_grid.py

OUTPUT:         C:\project\DSSVue-Example-Scripts\src\grids\grid.txt
DSSFILE:        C:\project\DSSVue-Example-Scripts\data\TC_0657.dss
PATHNAME:       /SHG/NECHES/PRECIP_TX_0657/04JUL2000:0000/04JUL2000:0100/PROJECTED_WGS84_ALBERS/
PRECISION:      -1

DSS Path Parts:
A Part: SHG
B Part: NECHES
C Part: PRECIP_TX_0657
D Part: 04JUL2000:0000
E Part: 04JUL2000:0100
F Part: PROJECTED_WGS84_ALBERS


    -----DSS---ZOPEN:  Existing File Opened,  File: C:\project\DSSVue-Example-Scripts\data\TC_0657.d                                         ss
                       Unit:    3;  DSS Versions - Software: 6-YO, File: 6-WE,  Library 7-IS
 -----DSS--- ZREAD Unit    3; Vers.    1:  /SHG/NECHES/PRECIP_TX_0657/04JUL2000:0000/04JUL2000:0100/                                         PROJECTED_WGS84_ALBERS/
 -----DSS--- ZREAD Unit    3; Vers.    1:  /SHG/NECHES/PRECIP_TX_0657/04JUL2000:0000/04JUL2000:0100/                                         PROJECTED_WGS84_ALBERS/
    -----DSS---zclose6 Unit:    3,   File: C:\project\DSSVue-Example-Scripts\data\TC_0657.dss
               Pointer Utilization:  0.28
               Number of Records:    313
               File Size:   1102.3  Kbytes
               Percent Inactive:   0.0
               Number of Reads:        8
DSS Path Parts:
A Part: SHG
B Part: NECHES
C Part: PRECIP_TX_0657
D Part: 04JUL2000:0000
E Part: 04JUL2000:0100
F Part: PROJECTED_WGS84_ALBERS


INPUT:          C:\project\DSSVue-Example-Scripts\src\grids\grid.txt
DSSFILE:        C:\project\DSSVue-Example-Scripts\src\grids\out.dss
PATHNAME:       /SHG/NECHES/PRECIP_TX_0657/04JUL2000:0000/04JUL2000:0100/PROJECTED_WGS84_ALBERS/
GRIDTYPE:       SHG
DTYPE:          PER-AVER
DUNITS:         inches

fromAscii: rows=181 cols=128
 minXindex=0 minYIndex=0
 cellsize=2000.0 llXCoord=0.0 llYCoord=712000.0
 noDataVal=-9999.0
processed 181 lines of data
processed 23168 values
origin set to 0, 356
Start Time: 4 July 2000, 00:00
  End Time: 4 July 2000, 01:00

14:58:21.728      -----DSS---zopen   Existing file opened,  File: C:\project\DSSVue-Example-Scripts\                                         src\grids\out.dss
14:58:21.728                         Handle 3;  Process: 32488;  DSS Versions - Software: 7-IS, File                                         :  7-IS
14:58:21.729                         Single-user advisory access mode
14:58:21.732 -----DSS--- zwrite  Handle 3;  Version 2:  /SHG/NECHES/PRECIP_TX_0657/04JUL2000:0000/04                                         JUL2000:0100/PROJECTED_WGS84_ALBERS/
14:58:21.733      -----DSS---zclose  Handle 3;  Process: 32488;  File: C:\project\DSSVue-Example-Scr                                         ipts\src\grids\out.dss
14:58:21.733                         Number records:         1
14:58:21.734                         File size:              15968  64-bit words
14:58:21.734                         File size:              124 Kb;  0 Mb
14:58:21.734                         Dead space:             0
14:58:21.736                         Hash range:             8192
14:58:21.736                         Number hash used:       1
14:58:21.737                         Max paths for hash:     1
14:58:21.737                         Corresponding hash:     7245
14:58:21.737                         Number non unique hash: 0
14:58:21.737                         Number bins used:       1
14:58:21.738                         Number overflow bins:   0
14:58:21.738                         Number physical reads:  9
14:58:21.738                         Number physical writes: 11
14:58:21.739                         Number denied locks:    0

C:\project\DSSVue-Example-Scripts\src\grids>






