#Miriam martín Sánchez
#Laura Gómez Bodego

#%%
from tkinter import *
import os
from instrument import *
import sounddevice as sd
from consts import *

def test():
    def callback(outdata, frames, time, status):    
        if status: print(status)    
        s = np.sum([i.next() for i in inputs],axis=0)
        s = np.float32(s)
        outdata[:] = s.reshape(-1, 1)

    tk = Tk()
    ins = Instrument(tk)
    inputs = [ins]
    

    # desactivar repeticion de teclas
    os.system('xset r off')

    stream = sd.OutputStream(samplerate=SRATE, channels=1, blocksize=CHUNK, callback=callback)    
    stream.start()
    tk.mainloop()

    # reactivar repeticion de teclas   
    os.system('xset r on')
    stream.close()

test()