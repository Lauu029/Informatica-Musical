'''
    wavetable real con clase python
    para conseguir la continuidad en los chunks generados y no tener pops
    llevamos un atributo "fase" que recorre la tabla de ondas y se actualiza 
    en cada sample producido.
    La siguiente vez se solicita un chunk, la fase está en el punto correcto
    Si varia la frencia de un chunk al siguiente, se varia el "paso" (step) entre 
    muestas de la wavetable, pero la fase está donde quedo -> enlazan dos senos de
    distinta frecuencia
'''

import numpy as np         # arrays    
import sounddevice as sd   # modulo de conexión con portAudio
import soundfile as sf     # para lectura/escritura de wavs

SRATE = 44100      
CHUNK = 64


class OscWaveTable:
    def __init__(self, frec, vol, size):
        self.frec = frec
        self.vol = vol
        self.size = size
        # un ciclo completo de seno en [0,2pi)
        t = np.linspace(0, 1, num=size)
        self.waveTable = np.sin(2 * np.pi * t)
        # arranca en 0
        self.fase = 0
        # paso en la wavetable en funcion de frec y RATE
        self.step = self.size/(SRATE/self.frec)

    def setFrec(self,frec): 
        self.frec = frec
        self.step = self.size/(SRATE/self.frec)

    def getFrec(self): 
        return self.frec    

    def setVol(self,vol): 
        self.vol = vol

    def getChunk(self):
        samples = np.zeros(CHUNK,dtype=np.float32)
        cont = 0 
        while cont < CHUNK:
            self.fase = (self.fase + self.step) % self.size
                                   
            x0 = int(self.fase) % self.size
            x1 = (x0 + 1) % self.size
            y0, y1 = self.waveTable[x0], self.waveTable[x1]            
            samples[cont] = y0 + (self.fase-x0)*(y1-y0)/(x1-x0)

            cont = cont+1
    
        return np.float32(self.vol*samples)
