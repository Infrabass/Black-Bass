
from pyo import *


class Midi:
    def __init__(self):
        #Trig Freeze
        self.m1 = Notein(poly=1, scale=1, first=11, last=11, channel=1, mul=1, add=0)
        self.sel1 = self.m1['trigon']
        #Part2
        self.m2 = Notein(poly=1, scale=1, first=14, last=14, channel=1, mul=1, add=0)
        self.sel2 = self.m2['trigon']
        self.m3 = Notein(poly=1, scale=1, first=12, last=12, channel=1, mul=1, add=0)
        self.sel3 = self.m3['trigon']
        #Start, active Inputs
        self.m4 = Notein(poly=1, scale=1, first=13, last=13, channel=1, mul=1, add=0)
        self.sel4 = self.m4['trigon']
        self.m5 = Notein(poly=1, scale=1, first=16, last=16, channel=1, mul=1, add=0)
        self.sel5 = self.m5['trigon']
        self.m6 = Notein(poly=1, scale=1, first=17, last=17, channel=1, mul=1, add=0)
        self.sel6 = self.m6['trigon']
        self.m7 = Notein(poly=1, scale=1, first=18, last=18, channel=1, mul=1, add=0)
        self.sel7 = self.m7['trigon']
        self.m8 = Notein(poly=1, scale=1, first=19, last=19, channel=1, mul=1, add=0)
        self.sel8 = self.m8['trigon']
        #Vol Grain
        self.cc1 = Midictl(ctlnumber = 28, minscale = 0, maxscale = 1, channel = 1)
        self.cc1.setInterpolation(False)
        self.hhcc3 = Midictl(ctlnumber = 2, minscale = 0, maxscale = 127, channel = 3)
        self.hhcc3.setInterpolation(False)
        self.pat = Pattern(self.send, time=0.05)
        self.tab = LinTable(list=[(0,0.0000),(31,0.7552),(91,0.5052),(108,0.3646),(128,0.0000)], size=128)
        self.tab.graph()
        

    def send(self):
        self.val = int(self.hhcc3.get())
        self.tabval = int(tab.get(self.val)*127)
        self.pat.getServer().ctlout(10, self.tabval)
        print self.tabval
    


