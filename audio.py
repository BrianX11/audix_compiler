from itertools import zip_longest

import math
import pyaudio
import struct

# Define la duracion de un paso en segundos, dado un tempo en BPM
def paso_duracion(tempo, step):
    tiempo_paso = 60.0 / tempo
    return tiempo_paso * step

# Convierte una nota en una frecuencia en Hz
def nota_frecuencia(nota):
    if nota == "S":
        return -1

    NOTAS = {'C': -9, 'C#': -8, 'D': -7, 'D#': -6, 'E': -5, 'F': -4, 'F#': -3, 'G': -2, 'G#': -1, 'A': 0, 'A#': 1, 'B': 2}
    A4 = 440.0  
    nota_nombre = nota[0].upper()
    nota_octava = int(nota[-1])
    distancia = NOTAS[nota_nombre] + (nota_octava - 4) * 12
    return A4 * math.pow(2.0, distancia / 12.0)

def convertir_a_iterable(valor):
    if isinstance(valor, str) or not isinstance(valor, (list, tuple)):
        return [valor]
    else:
        return valor
    
# Genera una onda sine de la lista de frecuencias y duracion especificadas
def generar_muestras(frecuencias, duracion, volumen, forma_de_onda='sine', ataque=0, decaimiento=1):
    frecuencias = convertir_a_iterable(frecuencias)
    frecuencia_muestreo = 44100
    duracion_muestras = int(duracion * frecuencia_muestreo)
    volumen_normalizado = volumen / (100.0 * len(frecuencias))

    # Genera las ondas sine para cada frecuencia
    ondas = []
    for frecuencia in frecuencias:

        if frecuencia == -1:
            volumen_normalizado = 0
            frecuencia = 0

        muestras = []
        for i in range(duracion_muestras):
            tiempo = i / frecuencia_muestreo

            # Calcula el factor de amplitud en base al ADSR
            if tiempo < ataque:
                factor_amplitud = tiempo / ataque
            elif tiempo < ataque + decaimiento:
                factor_amplitud = (decaimiento - (tiempo - ataque)) / decaimiento

            # Genera la muestra de la onda sine con el factor de amplitud
            if forma_de_onda == 'sine':
                valor = math.sin(2.0 * math.pi * frecuencia * i / frecuencia_muestreo)
            elif forma_de_onda == 'square':
                valor = math.copysign(1, math.sin(2.0 * math.pi * frecuencia * i / frecuencia_muestreo))
            elif forma_de_onda == 'triangle':
                valor = 2.0 * math.asin(math.sin(2.0 * math.pi * frecuencia * i / frecuencia_muestreo)) / math.pi
            elif forma_de_onda == 'saw':
                valor = math.atan(math.tan(math.pi * frecuencia * i / frecuencia_muestreo)) / math.pi

            muestra = valor * volumen_normalizado * factor_amplitud
            muestras.append(muestra)

        ondas.append(muestras)

    # Suma las muestras para todas las frecuencias
    muestras = [sum(par) for par in zip(*ondas)]

    # Devuelve la lista de muestras generadas
    return muestras

def generar_onda(muestras, stream):
    # Convierte las muestras a datos binarios
    datos = b''.join([struct.pack('f', valor) for valor in muestras])
    # Reproduce los datos binarios
    stream.write(datos)
    return datos

def reproducir(voces, bpm, volumen, forma_de_onda='sine'):
    p = pyaudio.PyAudio()
    formato = pyaudio.paFloat32
    canales = 1
    frecuencia_muestreo = 44100
    stream = p.open(format=formato,
                    channels=canales,
                    rate=frecuencia_muestreo,
                    output=True)
    m_voces = [[]]
    m_suma = []
    for voz in voces:
        for nota, duracion in voz:
            nota = nota_frecuencia(nota)
            duracion = paso_duracion(bpm, duracion)
            m_voces[-1].extend(generar_muestras(nota, duracion, volumen, forma_de_onda))
        m_voces.append([])
    m_voces.pop()
    max_idx = m_voces.index(max(m_voces))
    m_suma = [x * 1.0/len(m_voces) for x in m_voces[max_idx]]
    m_voces.pop(max_idx)
    m_total = []
    for i, m_voz in enumerate(m_voces):
        if m_total:
            m_suma = m_total
            m_total = []
        for sample1, sample2 in zip_longest(m_suma[:], m_voz, fillvalue=0):
            temp = sample1 + (sample2 * 1/(len(m_voces)+1))
            m_total.append(temp)
    generar_onda(m_total, stream)
    stream.stop_stream()
    stream.close()
    p.terminate()
