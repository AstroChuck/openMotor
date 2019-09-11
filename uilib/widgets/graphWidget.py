from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class GraphWidget(FigureCanvas):
    def __init__(self, parent):
        super(GraphWidget, self).__init__(Figure())
        self.setParent(None)
        self.setupPlot()
        self.setLabels()
        self.preferences = None

    def setPreferences(self, pref):
        self.preferences = pref

    def setupPlot(self):
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.plot = self.figure.add_subplot(111)
        self.figure.tight_layout()

    def setLabels(self):
        pass
        #elf.plot.set_xlabel('Time (s)')

    def plotData(self, simResult, xChannel, yChannels, grains):
        self.plot.clear()

        xAxisUnit = self.preferences.getUnit(simResult.channels[xChannel].unit)

        legend = []
        for channelName in yChannels:
            channel = simResult.channels[channelName]
            yUnit = self.preferences.getUnit(channel.unit)
            if channel.valueType in (list, tuple) and len(grains) > 0:
                data = []
                for frame in channel.getData(yUnit):
                    data.append([])
                    for grain in grains:
                        data[-1].append(frame[grain])
                self.plot.plot(simResult.channels[xChannel].getData(xAxisUnit), data)
            elif channel.valueType in (int, float):
                self.plot.plot(simResult.channels[xChannel].getData(xAxisUnit), channel.getData(yUnit))
            if channel.valueType in (int, float):
                if yUnit != '':
                    legend.append(channel.name + ' - ' + yUnit)
                else:
                    legend.append(channel.name)
            elif channel.valueType in (list, tuple):
                for i in range(len(channel.getData()[0])):
                    if i in grains:
                        if yUnit != '':
                            legend.append(channel.name + ' - Grain ' + str(i + 1) + ' - ' + yUnit)
                        else:
                            legend.append(channel.name + ' - Grain ' + str(i + 1))
        self.plot.legend(legend)
        self.plot.set_xlabel(simResult.channels[xChannel].name + ' - ' + xAxisUnit)
        self.plot.set_ylim(bottom=0)

    def saveImage(self, simResult, xChannel, yChannels, grains, path):
        self.plotData(simResult, xChannel, yChannels, grains)
        self.plot.set_title(simResult.getDesignation())
        self.figure.savefig(path, bbox_inches="tight")
        # Clear, but don't draw to not wipe away the graph in the UI
        self.plot.clear()

    def showData(self, simResult, xChannel, yChannels, grains):
        self.plotData(simResult, xChannel, yChannels, grains)
        self.draw()

    def resetPlot(self):
        self.plot.clear()
        self.draw()
