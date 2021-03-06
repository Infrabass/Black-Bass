
from pyo import *
import Resources._global as gl
import Resources.preferences as pref
import Resources.variables as vars
from Resources.midi_routing import Midi
from Resources.audio_class import Freeze, Granul, LorenzChaotic, RosslerChaotic
from Resources.misc_class import Inputs
from Resources.trigger_class import SoundTrigger

###Context###
context = 'maison'

if context == 'maison':
    pref.inputSysMic = 2

elif context == 'fac':
    pref.inputSysMic = 9
    

###Server###
s = Server(sr=48000, nchnls=pref.output_ch, buffersize=pref.buffer, duplex=1)
s.setMidiInputDevice(pref.midiIN)
s.setMidiOutputDevice(pref.midiOUT)
s.setInOutDevice(pref.output)

s.boot()
s.start()

gl.set('Server', s)

print pref.names[pref.position]
print 'Channels:', pref.output_ch
print 'Midi IN:', pref.midiIN
print 'Midi OUT:', pref.midiOUT
print 'Input Piezo:', pref.inputSysPiez
print 'Input Mic:', pref.inputSysMic

##Routing##
connect = CallAfter(pref.Connect, time=1)


###MIDI###
mid = Midi()

###Start###
inpPiez = Inputs(mid.t_0003, pref.input_pyo9)
inpMic = Inputs(mid.t_0003, pref.input_pyo10)
inpMicLive = Input(pref.input_pyo1)

###PART I###
##Intro Blast##
attd = AttackDetector(inpPiez.getOut(), maxthresh=6, minthresh=-32, reltime=0.1, mul=1, add=0).play()
fol1 = Follower2(inpPiez.getOut(), risetime=0.001, falltime=0.001, mul = 4).play()
envfol1 = Clip(fol1*2).play()

lrzGlitch = LorenzChaotic(pitch=RandInt(max=0.05, freq=0.9, mul=1, add=0), chaos=Randi(min=0.33, max=0.87, freq=0.85), cutoff=envfol1*4*8000, mul=envfol1*0.085)
lrzScream = LorenzChaotic(pitch=0.01, chaos=Randi(min=0.33, max=0.87, freq=0.85), cutoff=envfol1*4*8000, mul=envfol1*0.085)
gl.set('Glitch', lrzGlitch)
gl.set('Scream', lrzScream)

trig_intro = SoundTrigger('Audiofiles/Misc/BlackBass_IntroBlast.wav')


def Intro():
    trig_intro.Play()
    attd.stop()
    t_intro.stop()

t_intro = TrigFunc(attd, Intro)

##Freeze##
frez = Freeze(mid.t_0001, inpMicLive)
gra1 = Granul(frez.getOut(), vars.gran1_mul).out(0)
gra2 = Granul(frez.getOut(), vars.gran2_mul).out(2)
gra3 = Granul(frez.getOut(), vars.gran3_mul).out(4)
gra4 = Granul(frez.getOut(), vars.gran4_mul).out(6)

###PART II###
trig_part2 = SoundTrigger('Audiofiles/Misc/BlackBass_Part2Blast.wav')


def Part2():
    global frez, attd
    gra1.stop()
    gra2.stop()
    gra3.stop()
    gra4.stop()
    attd.setMaxthresh(3.5)
    attd.setMinthresh(-40)
    attd.setReltime(0.065)
    attd.play()
    fol1.play()
    envfol1.play()
    trig_part2.Play()
    frez.tabRec.reset()
    print '### PART II ###'

trigPart2 = TrigFunc(mid.t_0005, Part2)


##Attack Detection##
trig_clic = SoundTrigger('Audiofiles/SampleSoft/*.wav')
trig_impact = SoundTrigger('Audiofiles/SampleHard/*.wav')
trig_cb1 = SoundTrigger('Audiofiles/SampleCB_1/*.wav', envfol1*2, 1, 1, 1)
trig_cb2 = SoundTrigger('Audiofiles/SampleCB_2/*.wav', envfol1*2, 1, 1, 1)
trig_cb3 = SoundTrigger('Audiofiles/SampleCB_3/*.wav', envfol1*2, 1, 1, 1)
trig_cb4 = SoundTrigger('Audiofiles/SampleCB_4/*.wav', envfol1*2, 1, 1, 1)


def play():
    if envfol1.get() < 0.95:
        trig_clic.Pick()
        
    elif envfol1.get() > 0.95:
        trig_impact.Pick()
  
def cb_1():
    if random.randint(0,100) < 75:
        trig_cb1.Pick()
        print 'cb1'

def cb_2():
    if trig_lay_2 == 1 and random.randint(0,100) < 75:
        trig_cb2.Pick()
         print 'cb2'

def cb_3():
    if trig_lay_3 == 1 and random.randint(0,100) < 75:
        trig_cb3.Pick()
         print 'cb3'

def cb_4():
    if trig_lay_4 == 1 and random.randint(0,100) < 75:
        trig_cb4.Pick()
         print 'cb4'

#Grain
trig_grain = SoundTrigger('Audiofiles/Misc/BlackBass_Grain_AccuDispers_4.wav', mul=mid.cc1)
count_grain = 0

def GoGrain():
    global count_grain
    count_grain += 1
    if count_grain == 15:
        trig_grain.Play()
        count_grain.stop()



fol2 = Follower2(inpPiez.getOut(), risetime=0.02, falltime=0.02, mul=6, add=0).stop()
envfol2 = Clip(fol2*2.75).stop()
trig_bmath = SoundTrigger(path='Audiofiles/Misc/BlackMath_Follower2.wav', env=envfol1, mul=mid.cc1, rpan=0, fol=1)

def blackMath():
    global envfol2, trig_bmath
    fol2.play()
    envfol2.play()
    trig_bmath.Play()


t = TrigFunc(attd, play)
t_cb_1 = TrigFunc(attd, cb_1)
t_cb_2 = TrigFunc(attd, cb_2)
t_cb_3 = TrigFunc(attd, cb_3)
t_cb_4 = TrigFunc(attd, cb_4)
t_bmath = TrigFunc(mid.t_0905, blackMath)

trig_lay_2 = 0
trig_lay_3 = 0
trig_lay_4 = 0



def layer2():
    global trig_lay_2
    trig_lay_2 = 1

def layer3():
    global trig_lay_3
    trig_lay_3 = 1

def layer4():
    global trig_lay_4
    trig_lay_4 = 1
    

lay_2_Start = TrigFunc(mid.t_0901, layer2)
lay_3_Start = TrigFunc(mid.t_0902, layer3)
lay_4_Start = TrigFunc(mid.t_0903, layer4)

    
s.gui(locals())
