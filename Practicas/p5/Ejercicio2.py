#Miriam martín Sánchez
#Laura Gómez Bodego
#%%

from midiSequencerTk import *
import os    
from instrument import *
#%%
class PadInC(Instrument):
    def noteOn(self, midiNote):
        # Llama al método noteOn de la clase base para manejar la nota raíz
        super().noteOn(midiNote)

        # Calcula la quinta de la nota raíz
        if midiNote % 12 == 4 :
            fifth_midi_note = midiNote + 8 
        else :
            fifth_midi_note = midiNote + 7

        # Lanza la quinta
        super().noteOn(fifth_midi_note)
    def noteOff(self, midiNote): 
        super().noteOff(midiNote)

        # Calcula la quinta de la nota raíz
        if midiNote % 12 == 4 :
            fifth_midi_note = midiNote + 8 
        else :
            fifth_midi_note = midiNote + 7

        # Lanza la quinta
        super().noteOff(fifth_midi_note)

#%%
def test():
    def callback(outdata, frames, time, status):    
        if status: print(status)    
        #print(inputs)
        s = np.sum([i.next() for i in inputs],axis=0)
        s = np.float32(s)
        outdata[:] = s.reshape(-1, 1)

    os.system('xset r off')
    tk = Tk()
    ins = PadInC(tk)

    seq = MidiSequencerTk(tk,ins)
    #print(seq.seq)
    inputs = [ins]

    stream = sd.OutputStream(samplerate=SRATE, channels=1, blocksize=CHUNK, callback=callback)
    stream.start()

    tk.mainloop()

    stream.close()
    os.system('xset r on')

test()






# %%
