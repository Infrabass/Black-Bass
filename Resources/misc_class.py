
from pyo import *

class Inputs:
    def __init__(self, trig, input):
        self._trig = trig
        self._inputRAW = input
        self.fade = Fader(fadein=0.1, fadeout=0.1, dur=0, mul=1, add=0)
        self._input = Input(self._inputRAW, mul=self.fade)
        self.go = TrigFunc(self._trig, self.Start)

    def getOut(self):
        return self._input

    def Start(self):
        self.fade.play()
        print "Go"
        

        
    