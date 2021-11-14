import numpy as np

def quadraticMask(length, left_scale = 1):
    mask = np.linspace(0, 1, length)
    mask = mask ** left_scale
    mask = 1 - ((mask - 0.5) ** 2) * 4
    return mask

def exponentialMask(length, split = 0.1):
    length1 = int(length * split)
    length2 = length - length1
    mask1 = np.linspace(0, 1, length1)
    mask1 = 1 - ((mask1 - 1) ** 2)
    mask2 = np.linspace(0, 1, length2)
    mask2 = np.exp(- 5 * mask2 ** 1.3)
    mask = np.append(mask1, mask2)
    return mask

def waveSinWithMask(time_seq, frequency, stride_time):
    mask = quadraticMask(time_seq.shape[0], 0.5)
    wav = np.sin(2 * np.pi * frequency * time_seq) * mask
    return wav

def waveElectricGuitar(time_seq, frequency, stride_time):
    mask = exponentialMask(time_seq.shape[0], 0.05)
    wav = np.zeros_like(time_seq)
    # https://www.researchgate.net/figure/The-spectrum-of-an-ideal-electric-guitar-model-plucked-at-one-third-of-the-string-length_fig4_321787169
    weights = [1, 0.81, 0, 0.25, 0, 0, 0.24, 0.21, 0, 0, 0.1, 0, 0.13, 0.09, 0, 0.08, 0.1]
    frequency0 = frequency
    for weight in weights:
        wav += np.sin(2 * np.pi * frequency * time_seq) * weight
        frequency += frequency0
    wav /= np.max(np.abs(wav))
    wav *= mask
    return wav

if __name__ == '__main__':
    from matplotlib import pyplot as plt
    plt.plot(quadraticMask(1000))
    plt.plot(quadraticMask(1000, 0.5))
    plt.plot(quadraticMask(1000, 0.3))
    plt.plot(quadraticMask(1000, 0.25))
    plt.plot(exponentialMask(1000, 0.05))
    plt.show()
