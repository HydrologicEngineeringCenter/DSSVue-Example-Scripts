#  re-write a sheft file with some header lines

import sys


shf_file_output = open('c:/tmp/shef_with_header.shef','w')

shf_file_output.write(": Begin Header\n")
shf_file_output.write(": The header consists of the positional fields and the parameter\n")
shf_file_output.write(": The header consists of the positional fields and the parameter\n")
shf_file_output.write(": control string.  The body contains station identifiers and data \n")
shf_file_output.write(": with optional date/data overrides.  The terminator ends the entire\n")
shf_file_output.write(": \n")
		  
shf_file_input=open('C:\project\DSSVue-Example-Scripts\src\FolsomShefData.shef','r')

for line in shf_file_input:
	shf_file_output.write(line)

shf_file_input.close()
shf_file_output.close()