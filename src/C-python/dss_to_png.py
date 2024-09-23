import numpy as np
from hecdss import HecDss
from datetime import datetime

t1 = datetime(2020, 8, 1)
t2 = datetime(2020, 8, 31)

try:
    dss_file_path = r'sampleDssFile.dss'
    dss = HecDss(dss_file_path)

    tsElevPath = '/SHEYENNE RIVER/BALDHILL DAM/ELEV//1Hour/COMP/'
    tsc_elev = dss.get(tsElevPath)

    tsFlowPath = '/SHEYENNE RIVER/BALDHILL DAM/FLOW-OUT//1Hour/COMP/'
    tsc_flow = dss.get(tsFlowPath)
finally:
    dss.close()

########## plot it

import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots

pio.renderers
pio.renderers.default = "browser"

# make figure w/ 2 viewports
fig = make_subplots(rows=2, cols=1, shared_xaxes=True)

#########Top Viewport
# add elevations
fig.add_trace(go.Scatter(
    x=tsc_elev.times, y=tsc_elev.values, name='Elevation'))

# add flows
fig.add_trace(go.Scatter(
    x=tsc_flow.times, y=tsc_flow.values,
    name='Outflow', showlegend=True),
    row=2, col=1,
)
# set title
fig.update_layout(title='Reservoir Plot', showlegend=True)
# Set y-axes titles
fig.layout.yaxis1.update({'title': "<b>Elevation, ft NGVD29</b>"})
fig.layout.yaxis2.update({'title': "<b>Discharge, ft<sup>3</sup>/s</b>"})

# save plot
fig.write_image("sample.png")
# type fig in console to display interactive plot
fig.write_html("c:/temp/file.html")
