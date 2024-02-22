# %%
## Laura Gomez Bodego
## Miriam Martin Sanchez
import numpy as np

import sounddevice as sd
import soundfile as sf
import kbhit
 # %%
SRATE = 48000 # frecuencia de muestreo
CHUNK = 1024 # tamaño del bloque
 # %%

# # abrimos stream de entrada: InpuStream
# stream = sd.InputStream(samplerate=SRATE, blocksize=CHUNK, dtype=np.float32, channels=1)
# stream.start()
# # buffer para grabación.
# # (0,1): vacio (tamaño 0), 1 canal
# buffer = np.empty((0, 1), dtype="float32")
# kb = kbhit.KBHit()
# end = False
# c = ''
# while not end:
#     bloque, _check = stream.read(CHUNK) # devuelve un par (samples,bool)
#     buffer = np.append(buffer,bloque) # en bloque[0] están los samples
#     if kb.kbhit():
#         c = kb.getch()
#         if c == 'v':
#              end = True
       
# kb.set_normal_term()

# stream.stop()

# # reproducción del buffer adquirido
# c = input('Quieres reproducir [S/n]? ')
# if c!='n':
#     sd.play(buffer, SRATE)
#     sd.wait()
# # volcado a un archivo wav, utilizando la librería soundfile
# c = input('Grabar a archivo [S/n**? ')
# if c!='n':
#     sf.write("rec.wav", buffer, SRATE)


# %%
import numpy as np
import sounddevice as sd
import soundfile as sf
# Parámetros globales

CHUNK = 1024   # Tamaño del bloque de datos

def cargar_cancion(filename):
    data, samplerate = sf.read(filename)
    return data, samplerate
current_frame = 0
# Función callback

def callback(indata, outdata, frames,time, status):
    global current_frame
    global recording_frames
    global recording_started
    CHUNK=frames

    # Rellenar outdata con los samples de salida de la canción
    bloque = cancion[current_frame : current_frame+CHUNK]
    chunksize = bloque.shape[0]
    outdata[:chunksize,:] = bloque

    if recording_started:
        recording_frames.extend(indata[:, 0])  # Grabar solo un canal (mono)
    # loop de la cancion
    if chunksize < frames: # ha terminado?
        print('fin')
        outdata[chunksize:,:] = 0 # rellenamos con 0's el resto de outdata
        raise sd.CallbackStop()

    current_frame += chunksize
def start_recording():
    global recording_frames
    global recording_started
    recording_frames = []
    recording_started = True

def stop_recording(filename):
    global recording_frames
    global recording_started
    sf.write(filename, recording_frames, SRATE, subtype='FLOAT')
    recording_frames = []
    recording_started = False

cancion, SRATE = sf.read('entrada.wav',dtype=np.float32)
# Configurar el stream de salida con la función callback
stream = sd.Stream(
    samplerate=SRATE,
    channels=2,  # Dos canales para audio estéreo
    callback=callback,
    dtype=np.float32  # Tipo de datos de los samples de audio
)

# Iniciar la reproducción de la canción
recording_frames = []
recording_started = False
with stream:
    print('Reproduciendo...')
    start_recording()  # Comenzar la grabación
    input('Presiona Enter para detener la reproducción y la grabación\n')
    stop_recording('grabacion.wav')  # Detener la grabación y guardar el archivo