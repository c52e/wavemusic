import wave
import numpy as np
from base import *
from waves import *

canon_1_2_2_3 = '_1 -1 1 +1 *1 ^1'

BASE_FREQUENCY = 261.626
BASE_AMPLITUDE = 5000
STRIDE_TIME = 3
FRAMERATE = 44100

tune_map = {'1':0, '2':2, '3':4, '4':5, '5':7, '6':9, '7':11}

x1 = tuneToLogFrequency(canon_1_2_2_3, tune_map)

if __name__ == '__main__':
    durations = [STRIDE_TIME] * len(x1)
    wav = logFrequencysToWave(x1, durations, BASE_FREQUENCY, BASE_AMPLITUDE, STRIDE_TIME, FRAMERATE, waveKalimba)

    assert(np.max(wav) < 32768)
    assert(np.min(wav) >= -32768)
    wav_short = wav.astype('<i2') # short

    with wave.open("test.wav", 'wb') as wf:
        wf.setnchannels(1)
        wf.setframerate(FRAMERATE)
        wf.setsampwidth(2) # short
        wf.writeframes(wav_short.tobytes())
