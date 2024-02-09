# %%
##ej1
## Laura Gomez Bodego
## Miriam Martin Sanchez
#%%
import numpy as np
import sounddevice as sd
import kbhit
#%%
SRATE = 48000
CHUNK = 1024

# %%
class Osc:
    
    def __init__(self, frequency, volume, phase=0):
        self.frequency = frequency
        self.volume = volume
        self.phase = phase
        self.current_frame = 0
        
    def set_frequency(self, frequency):
        self.frequency = frequency

    def get_frequency(self):
        return self.frequency

    def set_volume(self, volume):
        self.volume = volume

    def get_volume(self):
        return self.volume

    def next(self):
        data = self.volume*np.sin(2*np.pi*(np.arange(self.current_frame,self.current_frame+CHUNK))*self.frequency/SRATE)
        self.current_frame += CHUNK # actualizamos ultimo generado
        return np.float32(data)
    
#%%

def testOsc():
    kb = kbhit.KBHit()

    numBloque = 0 # contador de bloques/chunks
    end = False # será true cuando el chunk esté incompleto o se pare la reproducción

    initial_frequency = 440.0  # Hz
    initial_volume = 1.0
    osc = Osc(initial_frequency, initial_volume)
    # stream de salida
    stream = sd.OutputStream( # creamos stream
        samplerate = SRATE, # frec de muestreo
        blocksize = CHUNK, # tamaño del bloque
        channels = 1) # num de canales
    stream.start() # arrancamos stream
    while not(end):
        
        bloque = osc.next()
     
        # Reproducir el chunk utilizando sounddevice
        
        if kb.kbhit():
            c = kb.getch() # variacion de volumen/abortar
            if (c=='v'): osc.set_volume(max(0,osc.get_volume()-0.05))
            elif (c=='V'):  osc.set_volume(min(1,osc.get_volume()+0.05))
            elif (c=='f') : osc.set_frequency(max(20,osc.get_frequency()-10))
            elif (c=='F') : osc.set_frequency(min(20000,osc.get_frequency()+10))
            elif c in ['q','escape']: end = True
        stream.write(bloque)
        print(f"\rVol: {osc.get_volume():.2f} bloque: {numBloque}",end='')
        #print(f"\rFrec: {osc.get_frequency():.2f} bloque: {numBloque}",end='')
        numBloque += 1
    kb.set_normal_term()
    stream.stop() # cerramos stream
    stream.close()


#%%
if __name__ == "__main__":
    testOsc()

# %%
