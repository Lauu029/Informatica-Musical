
#  Miriam Martín Sánchez

# Laura Gómez Bodego
#%%
#Ejercicio 4
import matplotlib.pyplot as plt
import numpy as np
import time
# gráficos en el notebook
%matplotlib inline
SRATE = 441000 # Sample rate, para todo el programa

#%%
# Oscilador
def osc(freq,dur=1,amp=1,phase=0, srate =  441000):
    # Calcula el tamaño del array en función de la duración y la tasa de muestreo
    size = int(dur * SRATE)
     # Calcula la señal sinusoidal con la frecuencia, amplitud y fase especificadas
    t = np.arange(size) / SRATE
    signal = amp * np.sin(2 * np.pi * freq * t + phase)
    
    return signal

#%%
# Modulador
def modulator(sample, freq):
    modulator_signal = osc(freq, len(sample)/SRATE, 1/2) + 0.5
    modulated_signal = sample * modulator_signal
    return modulated_signal

#%%
#ruido de entrada
dur = 1
noise = np.random.uniform(-1, 1, int(dur * SRATE))
mod_freq = 2  # Frecuencia del modulador
modulated_signal = modulator(noise, mod_freq)

#%%
# Representacion visual
# Dibujar la señal original y la señal modulada
plt.figure(figsize=(12, 6))
plt.plot(noise, label='Señal Original (Ruido)', color = 'm')
plt.plot(modulated_signal, label=f'Señal Modulada (Modulador {mod_freq} Hz)', color = 'c')
plt.title('Modulación de una Señal de Ruido')
plt.legend()
plt.show()
