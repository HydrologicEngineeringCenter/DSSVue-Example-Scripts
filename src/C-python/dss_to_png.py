#from datetime import datetime
from pydsstools.heclib.dss import HecDss
import numpy as np

def tscSplitter(path):
    'function to read data from dss and return list of times and values'
    global dssFile, startDay,startTime,endDay,endTime
    tsc = dssFile.read_window(path,startDay,startTime,endDay,endTime)
    times = tsc.pytimes
    values = list(tsc.values)
    return times, values

#time window
startDay = "01AUG2020"
startTime ="24:00"
endDay = "31AUG2020"
endTime = "24:00"
#dss path
dss_file_path = r'sampleDssFile.dss'
#ts path
tsElevPath = '/SHEYENNE RIVER/BALDHILL DAM/ELEV//1Hour/COMP/'
#open dss file
dssFile =  HecDss.Open(dss_file_path)
#get times and values with tscSplitter function
timeValue, elevValue = tscSplitter(tsElevPath)
#ts path
tsFlowPath = '/SHEYENNE RIVER/BALDHILL DAM/FLOW-OUT//1Hour/COMP/'
#get times and values with tscSplitter function
timeValue, flowValue = tscSplitter(tsFlowPath)
# close dss file
dssFile.close()

##########plot it

import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots
pio.renderers
pio.renderers.default = "browser"

#make figure w/ 2 viewports
fig  = make_subplots(rows=2, cols=1, shared_xaxes=True)

#########Top Viewport
# add elevations
fig.add_trace(go.Scatter(
    x=timeValue, y = elevValue, name='Elevation'))

# add flows
fig.add_trace(go.Scatter(
    x=timeValue, y=flowValue,
    name='Outflow', showlegend=True),
    row=2, col=1, 
             )
# set title
fig.update_layout( title='Reservoir Plot', showlegend=True)
# Set y-axes titles
fig.layout.yaxis1.update({'title': "<b>Elevation, ft NGVD29</b>"})
fig.layout.yaxis2.update({'title': "<b>Discharge, ft<sup>3</sup>/s</b>"})

# save plot
fig.write_image("sample.png")
#type fig in console to display interactive plot
fig.write_html("c:/temp/file.html")