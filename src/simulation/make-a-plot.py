from hec.heclib.dss import HecDss
from hec.script import Plot

def readData():
    startTime="18Jan1986 2400"
    endTime="18Mar1986 2400"
    dss = HecDss.open(R"C:\project\plot-dss-data\AR_Folsom_Simulation7.dss",startTime,endTime) 

    leakage = dss.read("//FOLSOM-DAM L&O/FLOW-DECISION//1Hour/E504-NAT--0/")
    eSpill = dss.read("//FOLSOM-EMERGENCY SPILLWAY/FLOW-DECISION//1Hour/E504-NAT--0/")
    mainSpill = dss.read("//FOLSOM-MAIN SPILLWAY/FLOW-DECISION//1Hour/E504-NAT--0/")
    dikes = dss.read("//FOLSOM-OVERFLOW/FLOW-DECISION//1Hour/E504-NAT--0/")
    power = dss.read("//FOLSOM-POWER PLANT/FLOW-DECISION//1Hour/E504-NAT--0/")
    lower = dss.read("//FOLSOM-RIVER OUTLETS - LOWER TIER/FLOW-DECISION//1Hour/E504-NAT--0/")
    upper = dss.read("//FOLSOM-RIVER OUTLETS - UPPER TIER/FLOW-DECISION//1Hour/E504-NAT--0/")
    # do math on data
    upper = upper.add(lower)
    power = power.add(upper)
    mainSpill = mainSpill.add(power)
    eSpill = eSpill.add(mainSpill)
    dikes = dikes.add(eSpill)
    leakage = leakage.add(dikes)
    # package up in dictionary
    allData = {
        'lower': lower.getData(),
        'upper': upper.getData(),
        'power': power.getData(),
        'mainSpill': mainSpill.getData(),
        'eSpill': eSpill.getData(),
        'dikes': dikes.getData(),
        'leakage': leakage.getData(),
    }
    return allData

def setCurveProperties(curve,color,fillType):
    curve.setFillColor(color)
    curve.setFillType(fillType)
    curve.setLineColor(color)


data = readData()
# make plot
plot = Plot.newPlot("Folsom Outflow")
plot.addData(data['leakage'])
plot.addData(data['dikes'])
plot.addData(data['eSpill'])
plot.addData(data['mainSpill'])
plot.addData(data['power'])
plot.addData(data['upper'])
plot.addData(data['lower'])

plot.showPlot()	# show the plot
# customize plot
setCurveProperties(plot.getCurve(data['lower']),'lightgreen','Below')
setCurveProperties(plot.getCurve(data['upper']),'lightblue','Below')
setCurveProperties(plot.getCurve(data['power']),'darkgreen','Below')
setCurveProperties(plot.getCurve(data['mainSpill']),'orange','Below')
setCurveProperties(plot.getCurve(data['eSpill']),'red','Below')
setCurveProperties(plot.getCurve(data['dikes']),'black','Below')
setCurveProperties(plot.getCurve(data['leakage']),'lightgray','Below')
