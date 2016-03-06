
from pyo import *
import Resources.variables as vars

class Midi:
    def __init__(self):
        self.sv = vars.get('Server')
        #Init Live
        self.sv.ctlout(21, 0, 2)    #Master Volume = MUTE
        self.sv.ctlout(0, 127, 10)  #DPA I ON
        self.sv.ctlout(1, 127, 10)  #DPA I Vol = 0   
        self.sv.ctlout(2, 64, 10)   #DPA I Pan = C
        self.sv.ctlout(3, 127, 10)  #Piez OFF
        self.sv.ctlout(4, 127, 10)  #Piez Vol = 0
        self.sv.ctlout(5, 64, 10)   #Piez Pan = C
        self.sv.ctlout(6, 36, 10)   #Blackhole size = 36
        self.sv.ctlout(7, 20, 10)   #Chain Select = Clean
        
        #Trig Freeze
        self.m_0001 = Notein(poly=1, scale=1, first=0, last=0, channel=2, mul=1, add=0)
        self.t_0001 = self.m_0001['trigon']
#        self.tf_0001 = TrigFunc(self.t_0001, self.Met_0001)
        #Toggle Saturation
        self.m_0002 = Midictl(ctlnumber = 102, minscale = 0, maxscale = 1, channel = 2)
        self.m_0002.setInterpolation(False)
        self.t_0002_ON = Select(self.m_0002, value=1, mul=1, add=0)
        self.t_0002_OFF = Select(self.m_0002, value=0, mul=1, add=0)
        self.tf_0002_ON = TrigFunc(self.t_0002_ON, self.Met_0002_ON)
        self.tf_0002_OFF = TrigFunc(self.t_0002_OFF, self.Met_0002_OFF)
        #Start, active Inputs
        self.m_0003 = Notein(poly=1, scale=1, first=1, last=1, channel=2, mul=1, add=0)
        self.t_0003 = self.m_0003['trigon']      
        #Part2
        self.m_0005 = Notein(poly=1, scale=1, first=3, last=3, channel=2, mul=1, add=0)
        self.t_0005 = self.m2['trigon']
        
        self.m3 = Notein(poly=1, scale=1, first=12, last=12, channel=1, mul=1, add=0)
        self.sel3 = self.m3['trigon']
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
        

#    def Met_0001(self):
    
    def Met_0002_ON(self):
        print 'banzai'
#        self.sig = SigTo(5, time=0.03, init=0.00, mul=1, add=0)
        self.sv.ctlout(7, 5, 10)   #Chain Select = Destroy
        
    def Met_0002_OFF(self):
#        self.sig = SigTo(5, time=0.03, init=0.00, mul=1, add=0)
        self.sv.ctlout(7, 20, 10)   #Chain Select = Clean

        

    def send(self):
        self.val = int(self.hhcc3.get())
        self.tabval = int(tab.get(self.val)*127)
        self.pat.getServer().ctlout(10, self.tabval)
        print self.tabval
    


