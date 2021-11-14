import numpy as np

def waveSinWithMask(time_seq, frequency, stride_time):
    mask = np.linspace(0, 1, time_seq.shape[0])
    mask = mask ** 0.5 # scale to left
    mask = 1 - ((mask - 0.5) ** 2) * 4
    wav = np.sin(2 * np.pi * frequency * time_seq) * mask
    return wav

def waveElectricGuitar(time_seq, frequency, stride_time):
    mask = np.linspace(0, 1, time_seq.shape[0])
    mask = mask ** 0.5 # scale to left
    mask = 1 - ((mask - 0.5) ** 2) * 4
    wav = np.zeros_like(time_seq)
    # https://www.researchgate.net/figure/The-spectrum-of-an-ideal-electric-guitar-model-plucked-at-one-third-of-the-string-length_fig4_321787169
    weights = [1, 0.81, 0, 0.25, 0, 0, 0.24, 0.21, 0, 0, 0.1, 0, 0.13, 0.09, 0, 0.08, 0.1]
    frequency0 = frequency
    for weight in weights:
        wav += np.sin(2 * np.pi * frequency * time_seq) * weight * 0.5
        frequency += frequency0
    wav *= mask
    return wav
