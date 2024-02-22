
from consts import *
import numpy as np         
import sounddevice as sd       
import matplotlib.pyplot as plt

class Osc:
    def __init__(self,freq=440.0,amp=1.0,phase=0.0, waveform= 'sin'):
        self.freq = freq
        self.amp = amp
        self.phase = phase
        self.frame = 0
        self.waveform = waveform


    def next(self):    
        sample = np.arange(self.frame, self.frame + CHUNK)
       # out = self.amp*np.sin(2*np.pi*(np.arange(self.frame,self.frame+CHUNK))*self.freq/SRATE)
        self.frame += CHUNK
        if self.waveform == 'sin':
            return self.amp * np.sin(2 * np.pi * self.freq * sample / SRATE)
        elif self.waveform == 'square':
            return self.amp * np.sign(np.sin(2 * np.pi * self.freq * sample / SRATE))
        elif self.waveform == 'triangle':
            return self.amp * np.arcsin(np.sin(2 * np.pi * self.freq * sample / SRATE)) * (2 / np.pi)
        elif self.waveform == 'sawtooth':
            return self.amp * (2 / np.pi) * np.arctan(1 / np.tan(np.pi * self.freq * sample / SRATE))
       # return out
    def setOnda(self, onda):
        self.waveform= onda