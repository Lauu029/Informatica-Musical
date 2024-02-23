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

def motion(event):
    global waveTable,stream,vol,frec, WIDTH, HEIGHT
    newFrec = event.x / WIDTH * (1000 - 100) + 100
    newVol = event.y / HEIGHT
    if (newFrec != frec):
        waveTable.setFrec( newFrec)
        frec = newFrec
    if (newVol != vol):
        waveTable.setVol( newVol)
        vol = newVol
    samples = waveTable.getChunk()
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
    print('{}, {}'.format(x, y))
    
main()
