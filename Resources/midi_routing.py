
from pyo import *
import Resources._global as gl
import variables as vars

class Midi:
    def __init__(self):
        self.sv = gl.get('Server')
        #Init Live
        self.sv.ctlout(21, 0, 2)    #Master Volume = MUTE
        self.sv.ctlout(0, 127, 10)  #DPA I ON
        self.sv.ctlout(1, 127, 10)  #DPA I Vol = 0db 
        self.sv.ctlout(2, 64, 10)   #DPA I Pan = C
        self.sv.ctlout(3, 0, 10)  #Piez OFF
        self.sv.ctlout(4, 127, 10)  #Piez Vol = 0db
        self.sv.ctlout(5, 64, 10)   #Piez Pan = C
        self.sv.ctlout(6, 36, 10)   #Blackhole size = 36
        self.sv.ctlout(7, 20, 10)   #Chain Select = Clean
        
        #0001 - Trig Freeze
        self.m_0001 = Notein(poly=1, scale=1, first=1, last=1, channel=2, mul=1, add=0)
        self.t_0001 = self.m_0001['trigon']
        self.tf_0001 = TrigFunc(self.t_0001, self.Met_0001)
        #0002 - Toggle Saturation
        self.m_0002 = Notein(poly=1, scale=1, first=2, last=2, channel=2, mul=1, add=0)
        self.t_0002 = self.m_0002['trigon']
        self.tf_0002 = TrigFunc(self.t_0002, self.Met_0002)
        self.count = 0
        #0003 - Start!
        self.m_0003 = Notein(poly=1, scale=1, first=3, last=3, channel=2, mul=1, add=0)
        self.t_0003 = self.m_0003['trigon']
        self.tf_0003 = TrigFunc(self.t_0003, self.Met_0003)    
        #0005 - Part2
        self.m_0005 = Notein(poly=1, scale=1, first=5, last=5, channel=2, mul=1, add=0)
        self.t_0005 = self.m_0005['trigon']
        #0901 - Trig2
        self.m_0901 = Notein(poly=1, scale=1, first=6, last=6, channel=2, mul=1, add=0)
        self.t_0901 = self.m_0901['trigon']
        #0902 - Trig3
        self.m_0902 = Notein(poly=1, scale=1, first=7, last=7, channel=2, mul=1, add=0)
        self.t_0902 = self.m_0902['trigon']
        #0903 - Trig4
        self.m_0903 = Notein(poly=1, scale=1, first=8, last=8, channel=2, mul=1, add=0)
        self.t_0903 = self.m_0903['trigon']
        #0905 - Start Textures Follow
        self.m_0905 = Notein(poly=1, scale=1, first=10, last=10, channel=2, mul=1, add=0)
        self.t_0905 = self.m_0905['trigon']
        #Vol Grain
        self.cc1 = Midictl(ctlnumber = 22, minscale = 0, maxscale = 1, channel = 1)
        self.cc1.setInterpolation(False)
        self.hhcc3 = Midictl(ctlnumber = 2, minscale = 0, maxscale = 127, channel = 3)
        self.hhcc3.setInterpolation(False)
        self.pat = Pattern(self.send, time=0.05)
        self.tab = LinTable(list=[(0,0.0000),(31,0.7552),(91,0.5052),(108,0.3646),(128,0.0000)], size=128)
        self.tab.graph()
        

    def Met_0001(self):
        print 'banzai'
    
    def Met_0002(self):
        self.count = (self.count+1)%2
        if self.count == 1:
            self.sv.ctlout(7, 5, 10)    #Chain Select = Destroy
            self.sv.ctlout(0, 0, 10)    #DPA I OFF
            self.sv.ctlout(3, 127, 10)  #Piez ON
            gl.get('Glitch').out(2)
            gl.get('Scream').out(6)
            vars.gran1_mul = 0.1
            vars.gran2_mul = 0.1
            vars.gran3_mul = 0.1
            vars.gran4_mul = 0.1
        else:
            self.sv.ctlout(7, 20, 10)   #Chain Select = Clean
            self.sv.ctlout(0, 127, 10)  #DPA I ON
            self.sv.ctlout(3, 0, 10)    #Piez OFF
            gl.get('Glitch').stop()
            gl.get('Scream').stop()
            vars.gran1_mul = 0.4
            vars.gran2_mul = 0.4
            vars.gran3_mul = 0.4
        
        
    def Met_0003(self):
        self.sv.ctlout(21, 127, 2)  #Master Volume = 0db
        

    def send(self):
        self.val = int(self.hhcc3.get())
        self.tabval = int(tab.get(self.val)*127)
        self.pat.getServer().ctlout(10, self.tabval)
        print self.tabval
    


