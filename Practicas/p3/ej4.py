# %%
##ej4
## Laura Gomez Bodego
## Miriam Martin Sanchez
#%%
import numpy as np
import sounddevice as sd
import time
#%%
SRATE = 48000
CHUNK = 1024

# %%
class Osc:
    
    def __init__(self, initial_frequency,final_frequency, volume,duration, phase=0):
        self.frequency = initial_frequency
        self.volume = volume
        self.phase = phase
        self.current_frame = 0
        self.initial_frequency = initial_frequency
        self.final_frequency = final_frequency
        self.duration = duration
        self.delta_frequency = (self.final_frequency - self.initial_frequency) / self.duration
        
    def set_frequency(self, frequency):
        self.frequency = frequency

    def get_frequency(self):
        return self.frequency

    def set_volume(self, volume):
        self.volume = volume

    def get_volume(self):
        return self.volume

    def next(self):
        self.frequency = self.initial_frequency + self.delta_frequency * self.current_frame / SRATE
        data = self.volume*np.sin(2*np.pi*(np.arange(self.current_frame,self.current_frame+CHUNK))*self.frequency/SRATE)
        self.current_frame += CHUNK # actualizamos ultimo generado
        return np.float32(data)
    def play(self, stream):
        timer=0
        # Calcular el deltaTime
       
        tiempo_anterior = time.time()
        while(timer<=self.duration):
            tiempo_actual = time.time()
            deltaTime = tiempo_actual - tiempo_anterior
            timer+=deltaTime
            bloque = self.next()
            stream.write(bloque)       
            tiempo_anterior = tiempo_actual
        
#%%

def testOsc():
    initial_frequency =1200.0  # Hz
    final_frequency =200
    duration= 3.0
    initial_volume = 1.0
    osc = Osc(initial_frequency,final_frequency, initial_volume,duration)
    # stream de salida
    stream = sd.OutputStream( # creamos stream
        samplerate = SRATE, # frec de muestreo
        blocksize = CHUNK, # tamaño del bloque
        channels = 1) # num de canales
    stream.start() # arrancamos stream       
    osc.play(stream)
   
    stream.stop() # cerramos stream
    stream.close()


#%%
if __name__ == "__main__":
    testOsc()

# %%
