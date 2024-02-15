# %%
##ej1
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
    def noteOn(self,frequency):
        self.frequency=frequency
        self.volume=1

    def noteOff(self):  
        self.volume=0 

    def next(self):
        data = self.volume*np.sin(2*np.pi*(np.arange(self.current_frame,self.current_frame+CHUNK))*self.frequency/SRATE)
        self.current_frame += CHUNK # actualizamos ultimo generado
        return np.float32(data)
#%%  
def obtener_frecuencia(nota):
    switch_notas = {
        'C': 523.251,
        'D': 587.33,
        'E': 659.255,
        'F': 698.456,
        'G': 783.991,
        'A': 880,
        'B': 987.767
    }

    # Convertir la nota a mayúscula para asegurarse de que coincida con las claves del diccionario
    nota1 = nota.upper()

    # Obtener la frecuencia de la nota ingresada
    frecuencia = switch_notas.get(nota1, None)

    # Si la nota no se encuentra en el diccionario, regresar None
    if frecuencia is None:
        return None

    # Verificar si la nota es minúscula para calcular la frecuencia de la octava inferior
    if nota.islower():
        frecuencia *= 2

    return frecuencia

 
#%%

def testOsc():

    partitura=[('G',0.5),('G',0.5),('A',1),('G',1),('c',1),('B',2),('G',0.5),('G',0.5),('A',1),('G',1)
               ,('d',1),('c',2),('G',0.5),('G',0.5),('g',1),('e',1),('c',1),('B',1),('A',1),('f',0.5),('f',0.5),('e',0.5)
               ,('c',1),('d',1),('c',2)]
    
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

    
    for nota, duracion in partitura:
        
        timer=0
        # Calcular el deltaTime
       
        tiempo_anterior = time.time()
        osc.noteOn(obtener_frecuencia(nota))
        while(timer<=duracion/2):
            tiempo_actual = time.time()
            deltaTime = tiempo_actual - tiempo_anterior
            timer+=deltaTime
            bloque = osc.next()
            stream.write(bloque)
            print(f"\rVol: {timer} bloque: {duracion}",end='')
            numBloque += 1
            tiempo_anterior = tiempo_actual
        pauseTime=0.05
        timer=0
        osc.noteOff()
        while(timer<=pauseTime/2):
            tiempo_actual = time.time()
            deltaTime = tiempo_actual - tiempo_anterior
            timer+=deltaTime
            bloque = osc.next()
            stream.write(bloque)
            print(f"\rVol: {timer} bloque: {pauseTime}",end='')
            numBloque += 1
            tiempo_anterior = tiempo_actual

        # Actualizar el tiempo anterior para la próxima iteración
       

        time.sleep(0.1)  # Puedes ajustar el tiempo de pausa según sea necesario
    stream.stop() # cerramos stream
    stream.close()


#%%
if __name__ == "__main__":
    testOsc()

# %%
