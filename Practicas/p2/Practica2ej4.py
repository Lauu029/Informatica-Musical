# %%
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
        left_data = self.volume * np.sin(2 * np.pi * (np.arange(self.current_frame, self.current_frame + CHUNK)) * self.frequency / SRATE)
        right_data = self.volume * np.sin(2 * np.pi * (np.arange(self.current_frame, self.current_frame + CHUNK)) * self.frequency / SRATE)

        stereo_data = np.empty((len(left_data), 2), dtype=np.float32)  # Crear un array vacío para almacenar datos estéreo
        stereo_data[:, 0] = np.float32(left_data)  # Canal izquierdo
        stereo_data[:, 1] = np.float32(right_data)  # Canal derecho

        self.current_frame += CHUNK  # Actualizamos el último generado
        return stereo_data
    

# %%
class Modulator(Osc):
    def __init__(self, frequency, volume, phase=0, min_value=-1, max_value=1, balance=0):
        super().__init__(frequency, volume, phase)
        self.min_value = min_value
        self.max_value = max_value
        self.balance = balance
    def get_balance(self):
        return self.balance
    
    def set_balance(self, balance):
        ## la variable balance solo puede estar en el rango -1 u 1 
        ## -1 canal izquierdo maximo
        ##1 canal derecho maximo
        self.balance = np.clip(balance, -1, 1)

    def next(self):
        data = super().next()
        left, right = data[:,0], data[:,1]
     
        stereo_data = np.empty((len(left), 2), dtype=np.float32)  # Crear un array vacío para almacenar datos estéreo
        stereo_data[:, 0]=np.float32(left);
        stereo_data[:, 1]=np.float32(right);
        if self.balance > 0:
            stereo_data[:, 0] = np.float32(left * (1 - self.balance))  # Canal izquierdo     
        else:
            stereo_data[:, 1] = np.float32(right * (1+ self.balance))  # Canal derecho
        return stereo_data
# %%
def testModulator():
    kb = kbhit.KBHit()

    numBloque = 0
    end = False

    initial_frequency = 440.0
    initial_volume = 1.0

    modulator = Modulator(initial_frequency, initial_volume)

    stream = sd.OutputStream(
        samplerate=SRATE,
        blocksize=CHUNK,
        channels=2  # Dos canales para señal estéreo
    )
    stream.start()

    while not end:
        bloque = modulator.next()

        if kb.kbhit():
            c = kb.getch()
            if c == 'v':
                modulator.set_volume(max(0, modulator.get_volume() - 0.05))
            elif c == 'V':
                modulator.set_volume(min(1, modulator.get_volume() + 0.05))
            elif c == 'f':
                modulator.set_frequency(max(20, modulator.get_frequency() - 10))
            elif c == 'F':
                modulator.set_frequency(min(20000, modulator.get_frequency() + 10))
            elif c == '+':
                modulator.set_balance(modulator.get_balance()+0.1)
            elif c == '-':
                modulator.set_balance(modulator.get_balance()-0.1)
            elif c in ['q', 'escape']:
                end = True
        
        bloque = bloque.astype(np.float32)
        stream.write(bloque)
        print(f"\rVol: {modulator.get_volume():.2f} Frec: {modulator.get_frequency():.2f} Balance: {modulator.get_balance():.2f} Bloque: {numBloque}", end='')
        numBloque += 1

    kb.set_normal_term()
    stream.stop()
    stream.close()

# %%
if __name__ == "__main__":
    testModulator()
# %%
