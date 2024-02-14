##
import numpy as np
import sounddevice as sd
CHUNK = 1024
def next (self):
    out=self.amp*np.sin(2*np.sin(2*np.arrange(self.fram,self.frame+CHUNK)))
##concatenacion de los next 
np.concatenate()
##como hacer el paneo :ej4

# %%
pan=0
end=false
while c!='q'and not end:
    bloque=data[numBloque*CHUNK:(numBloque+1)*CHUNK]
    left,right=bloque[:,0],bloque[:,1]
    p=0.5*pan/2
    left,right=np.sqrt(1-p)*left,np.sqrt(p)*right
    bloque=np.column_stack((left,right))
    stream.write(np.float32(bloque))

Stereo :
Una misma señal que esta cogida en distintas posiciones 
La señal mono sacaria una linea recta en el ejey la señal estero serian puntos al rededor del ejeY

FILTROS
le doy un chunk y me da un CHUNK modificado
cuando hay un desfase al apilcar un filtro->dar la vuelta a la señal aplicar de nuevo el
filtro e invertir de nuevo y esto hace que la señal ya no esta en desfase
    
