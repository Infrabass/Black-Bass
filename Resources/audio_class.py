
from pyo import *
import Resources.variables as vars

class Freeze:
    def __init__(self, trig, input, size=1.5, channel=1):
        self._trig = trig
        self._input = input
        self.size = size
        self.channel = channel
        
        self.callaft = None
        self.callaft2 = None
        self.count = 0

        #Wait rec time before new rec
        self.mdel = SDelay(Sig(0), delay = self.size)
        self.next = NextTrig(self._trig, self.mdel + Trig().play())
        self.mdel.input = self.next
        
        #Table Rec
        self.tabRec = NewTable(self.size, self.channel, feedback = 0.7)
        self.inp = TableRec(self._input, self.tabRec, fadetime=0.05)

        #Tab Temp
        self.tabsAlt = [NewTable(self.size, self.channel) for i in range(2)]

        #Tab to Read
        self.tabResult = NewTable(self.size, self.channel)

        #Table Morph
        self.fad = 0.2
        self.interp = Fader(fadein=self.fad, fadeout=self.fad, dur=0, mul=1, add=0).stop()
        self.morphle = TableMorph(self.interp, self.tabResult, self.tabsAlt).stop()
        
        self.trig = TrigFunc(self.next,self.rec)
        

    def rec(self):
        self.count = (self.count+1)%2
        self.inp.play()
        print "Rec!"
                
        self.callaft = CallAfter(self.startMorph, time=self.size, arg=None).play()
        
    def startMorph(self):
        self.morphle.play()
        self.tabsAlt[self.count].replace(self.tabRec.getTable(True))
        if self.count == 1:
            self.interp.play()
        else:
            self.interp.stop()
        print "Morph Start"
        
        self.callaft2 = CallAfter(self.postMorph, time=self.fad, arg=None).play()
        
    def postMorph(self):
        self.morphle.stop()
        print "Morph Stop"
        
    def getOut(self):
        return self.tabResult
        



class Granul:
    def __init__(self, input):
        self._input = input
        self.dens = Sig(Randi(40, 70, 0.11).play())
        self.pitch = Sig(Randi(0.995, 1.005, 0.23).play())
        self.pos = Sig(Randi(0.1, 0.6, 0.5).play(), mul=self._input.getSize()/2)
        self.dur = Sig(Randi(0.6, 1, 0.2).play())
        self.dev = Sig(Randi(0.05, 0.35, 0.35).play())
        self.pan = Sig(Randi(0, 1, 0.23).play())
        
        self.gran = Particle(self._input, HannTable(), dens=self.dens, pitch=self.pitch+Noise(0.01), pos=self.pos+Noise(1), dur=self.dur, dev=self.dev, pan=self.pan+Noise(0.480), chnls=2, mul=0.4, add=0)
        
    def out(self, x=0):
        self.gran.out(x)
        return self
        

        





