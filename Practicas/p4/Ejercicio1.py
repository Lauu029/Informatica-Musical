#Miriam martín Sánchez
#Laura Gómez Bodego

#%%

from tkinter import *
from tkinter import ttk
import os
import sounddevice as sd
from consts import *
import numpy as np   

import matplotlib.pyplot as plt
from consts import *
class Osc:
    def __init__(self,moduleOnda='sin',freq=440.0,amp=1.0,phase=0.0):
        self.freq = freq
        self.amp = amp
        self.phase = phase
        self.frame = 0
        self.moduleOnda=moduleOnda
    def setmoduleOnda(self,onda):
        self.moduleOnda=onda  
    def next(self):    
        sample = np.arange(self.frame, self.frame + CHUNK)
       # out = self.amp*np.sin(2*np.pi*(np.arange(self.frame,self.frame+CHUNK))*self.freq/SRATE)
        self.frame += CHUNK
        if self.moduleOnda == 'sin':
            return self.amp * np.sin(2 * np.pi * self.freq * sample / SRATE)
        elif self.moduleOnda == 'square':
            return self.amp * np.sign(np.sin(2 * np.pi * self.freq * sample / SRATE))
        elif self.moduleOnda == 'triangle':
            return self.amp * np.arcsin(np.sin(2 * np.pi * self.freq * sample / SRATE)) * (2 / np.pi)
        elif self.moduleOnda == 'sawtooth':
            return self.amp * (2 / np.pi) * np.arctan(1 / np.tan(np.pi * self.freq * sample / SRATE))

class OscFM:
    def __init__(self,carrieOnda='sin',moduleOnda='sawtooth',fc=110.0,amp=1.0,fm=6.0, beta=1.0):
        self.fc = fc
        self.amp = amp
        self.fm = fm
        self.beta = beta
        self.frame = 0
        self.carrieOnda = carrieOnda
        self.moduleOnda=moduleOnda

        # moduladora = βsin(2πfm)
        self.mod = Osc(freq=fm,amp=beta,moduleOnda=moduleOnda)
    def setcarrieOnda(self,onda):
        self.carrieOnda=onda   
    def setmoduleOnda(self,onda):
        self.moduleOnda=onda 
        self.mod.setmoduleOnda(onda) 
    def next(self):  
        # sin(2πfc+mod)  
        # sacamos el siguiente chunk de la moduladora
        mod = self.mod.next()

        # soporte para el chunk de salida
        sample = np.arange(self.frame,self.frame+CHUNK)        
        # aplicamos formula
        if self.carrieOnda=='sin':
            out =  self.amp*np.sin(2*np.pi*self.fc*sample/SRATE + mod)
        elif self.carrieOnda=='square':
            out = self.amp * np.sign(np.sin(2 * np.pi * self.fc * sample / SRATE+mod))
        elif self.carrieOnda=='triangle':
            out = self.amp * np.arcsin(np.sin(2 * np.pi * self.fc * sample / SRATE+mod)) * (2 / np.pi)
        elif self.carrieOnda=='sawtooth':
            out = self.amp * (2 / np.pi) * np.arctan(1 / np.tan(np.pi * self.fc * sample / SRATE+mod))
        self.frame += CHUNK
        return out 
carrier='sin'
module='sin'    
def test():
    global module,carrier
    root = Tk()
    root.geometry("600x600")  # Establecer el tamaño de la ventana
    ##root.bind('<Motion>', motion)

    frm = ttk.Frame(root, padding=10)
    frm.grid()
  
    end = False # será true cuando el chunk esté incompleto o se pare la reproducción

    ##osc.setcarrieOnda('sierra')
    # stream de salida
    stream = sd.OutputStream( # creamos stream
        samplerate = SRATE, # frec de muestreo
        blocksize = CHUNK, # tamaño del bloque
        channels = 1) # num de canales
    stream.start() # arrancamos stream
    def handle_selection(event):
        global module,carrier
        print("Selección:", combo1.get(), combo2.get())
        carrier= combo1.get()
        module=combo2.get()
    label1 = ttk.Label(frm, text="Carrier:")
    label1.grid(row=0, column=0, padx=5, pady=5)
    # Primer Combobox
    combo1 = ttk.Combobox(frm, values=["sin", "square", "triangle","sawtooth"])
    combo1.grid(row=1, column=0, padx=5, pady=5)
    combo1.bind("<<ComboboxSelected>>", handle_selection)

    label2 = ttk.Label(frm, text="Module:")
    label2.grid(row=2, column=0, padx=5, pady=5)
    # Segundo Combobox
    combo2 = ttk.Combobox(frm, values=["sin", "square", "triangle","sawtooth"])
    combo2.grid(row=3, column=0, padx=5, pady=5)
    combo2.bind("<<ComboboxSelected>>", handle_selection)
    root.mainloop()
# concatenamos 3 chunks y dibujamos
    o = OscFM(carrieOnda=carrier,moduleOnda=module,fc=20,fm=1000,beta=0.1)

# concatenamos 3 chunks y dibujamos
    sgn = np.zeros(0)
    for i in range(3):
        sgn = np.concatenate((sgn,o.next()))
    plt.plot(sgn)
    plt.show() 
    while not(end):       
        bloque = o.next()
        stream.write(np.float32(bloque))
             
    stream.stop() # cerramos stream
    stream.close()

    return 1

test()






# %%
