#%%
import numpy as np
import sounddevice as sd   # modulo de conexión con portAudio
import soundfile as sf     # para lectura/escritura de wavs
from tkinter import *
from tkinter import ttk



WIDTH = 600 # ancho y alto de la ventana de PyGame
HEIGHT = 600

SRATE = 44100      
CHUNK = 64
 
class OscWaveTable:
    def __init__(self, frec, vol, size):
        self.volume = vol
        self.fequency = frec
        self.rate = size
        c = np.linspace(0, 1, num=size)
        self.wavetable = np.sin(2 * np.pi * c)
        self.fase = 0
        self.step = self.rate/(SRATE/self.fequency)

    def setFrequency(self,frec): 
        self.fequency = frec
        self.step = self.rate/(SRATE/self.fequency)

    def getFrequency(self): 
        return self.fequency    

    def setVol(self,vol): 
        self.volume = vol

    def next(self):
        samples = np.zeros(CHUNK, dtype=np.float32)
        indices = (np.arange(CHUNK) * self.step + self.fase) % self.rate
        x0 = indices.astype(int) % self.rate
        x1 = (x0 + 1) % self.rate
        y0, y1 = self.wavetable[x0], self.wavetable[x1]
        interp_weights = indices - x0
        samples = y0 + interp_weights * (y1 - y0) / (x1 - x0)
        self.fase = (self.fase + CHUNK * self.step) % self.rate
        return np.float32(self.volume * samples)
       

def motion(event):
    global waveTable,stream,vol,frec
    newFrec = event.x / 600 * (1000 - 100) + 100
    newVol = event.y / 600
    if (newFrec != frec):
        waveTable.setFrequency( newFrec)
        frec = newFrec
    if (newVol != vol):
        waveTable.setVol( newVol)
        vol = newVol
    samples = waveTable.next()
    stream.write(np.float32(0.5 * samples))
    

def main():
    global waveTable,stream,vol,frec
    frec = 800
    vol = 1.0
    stream = sd.OutputStream(samplerate=SRATE, blocksize=CHUNK, channels=1)
    stream.start()
    waveTable = OscWaveTable(frec, vol, SRATE)
    root = Tk()
    root.geometry("600x600")  # Establecer el tamaño de la ventana
    root.bind('<Motion>', motion)

    frm = ttk.Frame(root, padding=10)
    frm.grid()
    root.mainloop()
    stream = sd.OutputStream(samplerate=SRATE,blocksize=CHUNK,channels=1)  
    stream.start()

    
main()


# %%
