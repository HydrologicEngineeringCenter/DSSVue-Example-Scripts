from hec.script import Plot, MessageBox, AxisMarker
from hec.heclib.dss import HecDss, DSSPathname
from hec.gfx2d import LegendPanel
import java
from hec.script.Constants import TRUE, FALSE

path='C:/project/DSSVue-Ch8-Example-Scripts/src/Legend-Position/'

dssFile=HecDss.open(path+"7_PMF_P50_fc_H250.dss", "02Jan2000 0600", "03Jan2000 0600")

Precip=dssFile.read("//WP-050/PRECIP-INC//5MIN/RUN:7_PMF_P50_FC_H250/")
Q_in250=dssFile.read("//DS-19/FLOW-COMBINE//5MIN/RUN:7_PMF_P50_FC_H250/")
Q_out250=dssFile.read("//DS-19/FLOW//5MIN/RUN:7_PMF_P50_FC_H250/")
Elev_250=dssFile.read("//DS-19/ELEVATION//5MIN/RUN:7_PMF_P50_FC_H250/")

dssFile=HecDss.open(path+"7_PMF_P50_fc_H400.dss", "02Jan2000 0600", "03Jan2000 0600")
Q_out400=dssFile.read("//DS-19/FLOW//5MIN/RUN:7_PMF_P50_FC_H400/")
Elev_400=dssFile.read("//DS-19/ELEVATION//5MIN/RUN:7_PMF_P50_FC_H400/")

dssFile=HecDss.open(path+"7_PMF_P50_fc_H550.dss", "02Jan2000 0600", "03Jan2000 0600")
Q_out550=dssFile.read("//DS-19/FLOW//5MIN/RUN:7_PMF_P50_FC_H550/")
Elev_550=dssFile.read("//DS-19/ELEVATION//5MIN/RUN:7_PMF_P50_FC_H550/")

datasets = [ ]
datasets.append(Precip); datasets.append(Q_in250); datasets.append(Q_out250); datasets.append(Elev_250)
datasets.append(Q_out400); datasets.append(Elev_400)
datasets.append(Q_out550); datasets.append(Elev_550)

plot=Plot.newPlot("DS-19 Most Reasonable PMF - Adopted")
layout=Plot.newPlotLayout()
TopView=layout.addViewport(30.)
#lp = LegendPanel(None,LegendPanel.VERTICAL_LAYOUT)
#lp.setLegendPosition(LegendPanel.VIEWPORT_LEGEND_UPPER_LEFT)
#lp.addViewport(TopView)

#lp = plot.getLegend()
#print 'name = ',lp.getClass().getName()


#print dir (lp)
#print type(lp)
#lp.setLegendPosition(LegendPanel.VIEWPORT_LEGEND_UPPER_LEFT)

#LegendPanel.this._parent.moveLegendToPosition(LegendPanel.VIEWPORT_LEGEND_UPPER_LEFT)

#layout = plot.getPlotLayout()
#layout. = LegendPanel.VIEWPORT_LEGEND_UPPER_LEFT
#plot.buildComponents(layout) #;

MidView=layout.addViewport(50.)
BottomView=layout.addViewport(50.)

TopView.addCurve("Y1", Precip.getData())

MidView.addCurve("Y1", Elev_250.getData())
MidView.addCurve("Y1", Elev_400.getData())
MidView.addCurve("Y1", Elev_550.getData())

BottomView.addCurve("Y1", Q_in250.getData())
BottomView.addCurve("Y1",Q_out250.getData())
BottomView.addCurve("Y1",Q_out400.getData())
BottomView.addCurve("Y1",Q_out550.getData())

plot.configurePlotLayout(layout)
plot.setSize(700,1000)

plot.showPlot()

plot.getLegendLabel(Precip.getData()).setText("PMF Precipitation (5-min)")
plot.getLegendLabel(Q_in250.getData()).setText("PMF Inflow")
plot.getLegendLabel(Q_out250.getData()).setText("PMF Outflow - 250 ft Spillway")
plot.getLegendLabel(Elev_250.getData()).setText("PMF Elev - 250 ft Spillway")
plot.getLegendLabel(Q_out400.getData()).setText("PMF Outflow - 400 ft Spillway")
plot.getLegendLabel(Elev_400.getData()).setText("PMF Elev - 400 ft Spillway")
plot.getLegendLabel(Q_out550.getData()).setText("PMF Outflow - 550 ft Spillway")
plot.getLegendLabel(Elev_550.getData()).setText("PMF Elev - 550 ft Spillway")

plot.getViewport(0).getAxis("Y1").setReversed(False)
plot.getCurve(Precip).setFillColor("lightblue")
plot.getCurve(Precip).setFillType("Above")

plot.getCurve(Precip).setLineColor("blue")
plot.getCurve(Q_in250).setLineColor("black")
plot.getCurve(Q_out250).setLineColor("magenta")
plot.getCurve(Elev_250).setLineColor("magenta")
plot.getCurve(Q_out400).setLineColor("gray")
plot.getCurve(Elev_400).setLineColor("gray")
plot.getCurve(Q_out550).setLineColor("blue")
plot.getCurve(Elev_550).setLineColor("blue")

plot.setPlotTitleText("DS-19 Most Reasonable PMF - Spillway Crest 1183.6 ft-NAVD88")
title = plot.getPlotTitle()
title.setFont("Arial Black")
title.setFontSize(30)
plot.setPlotTitleVisible(TRUE)

#if self.rdbtnUpperRightOf.isSelected():
#legendLocation = 'Viewport Top Right'
#if self.rdbtnUpperLeftOf.isSelected():
#legendLocation = 'Viewport Top Left'
#if self.rdbtnBottomOfPlot.isSelected():
#legendLocation = 'Bottom'

plot.setLegendLocation('Viewport Top Left')
