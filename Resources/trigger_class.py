
from pyo import *
import glob
import random


class SoundTrigger:
    def __init__(self, env, path, mul=1, rpan=0, fol=0):
        self._env = env
        self._path = glob.glob(path)
        self._mul = mul
        self.rpan = rpan
        self.fol = fol
        self.nbSnd = len(self._path)
        self.tab = [SndTable(p) for p in self._path]
        self.mTrig = Trig().stop()
        self.trigTab = TrigEnv(input=self.mTrig, table=self.tab[0], dur=self.tab[0].getDur(), mul = self._mul).play()
        if self.fol == 0:
            if self.rpan == 0:
                self.trigTab.out(2)
            else:
                self.pan = SPan(self.trigTab, outs=2, pan=0.50, mul=self._mul).out(2)
        else:
            if self.rpan == 0:
                self.trigTab.mul = self._env
                self.trigTab.out(2)
            else:
                self.pan = SPan(self.trigTab, outs=2, pan=0.50, mul=self._env).out(2)
        

    def Pick(self):
        if self.rpan == 1:
            self.rPan.pan = random.uniform(0,1)
        self.pick = random.randint(0,self.nbSnd-1)
        self.durPick = self.tab[self.pick].getDur()
        self.trigTab.setTable(self.tab[self.pick])
        self.trigTab.setDur(self.durPick)
        self.mTrig.play()
        
    def Play(self):
        if self.rpan == 1:
            self.pan.pan = random.uniform(0,1)
        self.mTrig.play()
        print 'Play'
            
    def SendTrig(self):
        return self.mTrig
        

        