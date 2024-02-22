
import numpy as np 

import osc
import matplotlib.pyplot as plt
from consts import *


class OscFM:
    def __init__(self,fc=110.0,amp=1.0,fm=6.0, beta=1.0, carrier_waveform='sin', modulator_waveform='sin'):
        self.fc = fc
        self.amp = amp
        self.fm = fm
        self.beta = beta
        self.frame = 0
        self.carrier_waveform=carrier_waveform
        self.modulator_waveform= modulator_waveform
        # moduladora = βsin(2πfm)
        self.mod = Osc(freq=fm,amp=beta, waveform= self.modulator_waveform)
        
    def next(self):  
        # sacamos el siguiente chunk de la moduladora
        mod = self.mod.next()

        # soporte para el chunk de salida
        sample = np.arange(self.frame,self.frame+CHUNK)        
        # aplicamos formula
    
        if self.carrier_waveform == 'sin':
            out= self.amp * np.sin(2 * np.pi * self.fc * sample / SRATE +mod)
        elif self.carrier_waveform == 'square':
             out = self.amp * np.sign(np.sin(2 * np.pi * self.fc * sample / SRATE+mod))
        elif self.carrier_waveform == 'triangle':
             out = self.amp * np.arcsin(np.sin(2 * np.pi * self.fc * sample / SRATE+mod)) * (2 / np.pi)
        elif self.carrier_waveform == 'sawtooth':
             out = self.amp * (2 / np.pi) * np.arctan(1 / np.tan(np.pi * self.fc * sample / SRATE+mod))
        self.frame += CHUNK
        return out 
        
       
    def changeOnda(self, o):
        self.carrier_waveform = o

    def changeOndaMod(self, oMod):
        self.modulator_waveform = oMod
        self.mod.setOnda(oMod)