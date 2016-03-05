
from pyo import *
import os


###Soundcard Settings###
output_ch = 10
midiIN = 99
midiOUT = 99
inputSysPiez = 1
inputSysMic = 9
input_pyo1 = 0
input_pyo2 = 1
input_pyo9 = 8
input_pyo10 = 9



names, indexes = pa_get_output_devices()
position = names.index("JackRouter")
output = indexes[position]



###Connection###
app = 'Live'

def Connect():
    #Sys Input to Pyo & App
    os.system('jack_connect system:capture_%s Python:in9' %inputSysPiez)
    os.system('jack_connect system:capture_%s Python:in10' %inputSysMic)
    os.system('jack_connect system:capture_%s %s:in9' %(inputSysPiez, app))
    os.system('jack_connect system:capture_%s %s:in10' %(inputSysMic, app))
    #App to Pyo
    os.system('jack_connect %s:out9 Python:in1' %app)
#    os.system('jack_connect %s:out10 Python:in2' %app)
    #Pyo to App
    os.system('jack_connect Python:out1 %s:in1' %app)
    os.system('jack_connect Python:out2 %s:in2' %app)
    os.system('jack_connect Python:out3 %s:in3' %app)
    os.system('jack_connect Python:out4 %s:in4' %app)
    os.system('jack_connect Python:out5 %s:in5' %app)
    os.system('jack_connect Python:out6 %s:in6' %app)
    os.system('jack_connect Python:out7 %s:in7' %app)
    os.system('jack_connect Python:out8 %s:in8' %app)
    #App to Sys Output
    os.system('jack_connect %s:out1 system:playback_1' %app)
    os.system('jack_connect %s:out2 system:playback_2' %app)





