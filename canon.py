import wave
import numpy as np

def tuneToLogFrequency(source, tune_map):
    log_frequencys = []
    oct = 0
    for tune in source:
        if tune in ' \t\r\n':
            continue
        elif tune == '^':
            oct = 36
        elif tune == '*':
            oct = 24
        elif tune == '+':
            oct = 12
        elif tune == '-':
            oct = -12
        elif tune == '_':
            oct = -24
        elif tune == '.':
            oct = -36
        else:
            log_frequencys.append(oct + tune_map[tune] if tune != '0' else None)
            oct = 0
    return log_frequencys

canon_1_2_2_3 = [
# https://www.everyonepiano.com/Number-31-1-Canon-Pachelbels-Canon-Numbered-Musical-Notation-Preview-1.html
'''
 0 0 0 0 0 0 0 0   0 0 0 0 0 0 0 0   0 0 0 0 0 0 0 0   0 0 0 0 0 0 0 0
+3 0 0 0+2 0 0 0  +1 0 0 0 7 0 0 0   6 0 0 0 5 0 0 0   6 0 0 0 7 0 0 0
+3 0 0 0+2 0 0 0   0 0 0 0 0 0 0 0   0 0 0 0 0 0 0 0   6 0 0 0 5 0 0 0
 0 0 0 0 0 0 0 0   0 0 0 0 0 0 0 0   0 0 0 0 0 0 0 0   0 0 0 0 0 0 0 0
 0 0 0 0 0 0 0 0   0 0 0 0 0 0 0 0   0 0 0 0 0 0 0 0   0 0 0 0 0 0 0 0
 0 0 0 0 0 0 0 0   0 0 0 0 0 0 0 0   0 0 0 0 0 0 0 0   6 0 0 0 0 0 0 0
 0 0 0 0 0 0 0 0   0 0 0 0 0 0 0 0   0 0 0 0 0 0 0 0   6 0 0 0 0 0 0 0
 0 0 0 0 0 0 0 0   0 0 0 0 0 0 0 0   0 0 0 0 0 0 0 0   0 0 0 0 0 0 0 0
 0 0 0 0 0 0 0 0   0 0 0 0 0 0 0 0   0 0 0 0 0 0 0 0   0 0 0 0 0 0 0 0
 0 0 0 0 0 0 0 0   0 0 0 0 0 0 0 0   0 0 0 0 0 0 0 0   0 0 0 0 0 0 0 0
 0 0 0 0 0 0 0 0   0 0 0 0 0 0 0 0   0 0 0 0 0 0 0 0   0 0 0 0 0 0 0 0
 0 0 0 0 0 0 0 0   0 0 0 0 0 0 0 0   0 0 0 0 0 0 0 0   0 0 0 0 0 0 0 0
 0 0 0 0 0 0 0 0   0 0 0 0 0 0 0 0   0 0 0 0 0 0 0 0   0 0 0 0 0 0 0 0
+3 0 0 0 0 0 0 0   0 0 0 0 0 0 0 0   0 0 0 0 0 0 0 0   0 0 0 0 0 0 0 0
+3 0 0 0 0 0 0 0  +3 0 0 0 0 0 0 0  +1 0 0 0 0 0 0 0   6 0 0 0 0 0 0 0
+3 0 0 0 0 0 0 0  +3 0 0 0 0 0 0 0  +1 0 0 0 0 0 0 0   6 0 0 0 0 0 0 0
 0 0 0 0 0 0 0 0   0 0 0 0 0 0 0 0   0 0 0 0 0 0 0 0   0 0 0 0 0 0 0 0
 0 0 0 0 0 0 0 0   0 0 0 0 0 0 0 0   0 0 0 0 0 0 0 0   0 0 0 0 0 0 0 0
+1 0 0 0 0 0 0 0
'''
,
'''
 3 0 0 0 2 0 0 0   1 0 0 0-7 0 0 0  -6 0 0 0-5 0 0 0  -6 0 0 0-7 0 0 0
 5 0 0 0 5 0 0 0   3 0 0 0 3 0 0 0   1 0 0 0 1 0 0 0   1 0 0 0 2 0 0 0
 5 0 0 0 5 0 4 0  +1 0 0 0 7 0 5 0   6 0 0 0 5 0 3 0   4 0 0 0 2 0 4 0
+1 7+1 3 5 0 7 0  +1 0+3 0+5+3+5+6  +4+3+2+4+3+2+1 7   6 4+1 0 7 5+1 7
+1 7+1 3 5 0 7 0  +1 0+3 0+5+3+5+6  +4+3+2+4+3+2+1 7   6 5 4 0+1 0 7+2
+3 0+3+1 0 0+4+2  +1 0+1 7 7 5 3 5   6 0 7+1 5 0 3 5   4 0 4+1+1 0 7+2
+3 0+3+1 0 0+4+2  +1 0+1 7 7 5 3 5   6 0 7+1 5 0 3 5   4 0 4+1+1 0 7+2
+5+3+5+3+5 6+1+3  +3+1+3 3 5 5 5 7   6+1 6 5 5 3 5 7   6+1+1 7 7 7+2+4
+5+3+5+3+5 6+1+3  +3+1+3 3 5 5 5 7   6+1 6 5 5 3 5 7   6+1+1 7 7 7+2+4
+3+1+3+2+2+1+3+1  +1 6+1 1 3 3 3 7   6+1 6 5 5 3 5 7   6+1+1 7 7+2 7 6
+1 0 0 0 0 0 0 0   0 0 0 0 0 0 0 0   0 0 0 0 0 0 0 0   0 0 0 0 0 0 0 0
 0+3+5+3 0+2+4+2   0+1+3+1 0+3+1 7   0 6+1 6 0 5+1 5   0 6+1 7 0 6+2 7
 0+3+5+3 0+2+4+2   0+1+3+1 0+5+3+5  +6+6+4+6+5+5+3+5  +6+4+5+6+7+5 7+2
 5 0+3+1 0 0+3+2  +2 0+1 7 3 7+3+7  +7+5+5+3+3+1+1 6   6 4 6 6 7 5+1+2
+1 0+3+4+5+6+5+4  +1 0+1+2+3+4+3+2   4 0 6+1+1 0+1 7   4 0 4+1+1 0 7+2
+1 0+3+4+5+6+5+4  +1 0+1+2+3+4+3+2   4 0 6+1+1 0+1 7   4 0 4+1+1 0 7+2
+3 0 0 0+2 0 0 0  +1 0 0 0 7 0 0 0   6 0 0 0 5 0 0 0   6 0 0 0 7 0 0 0
+3 0 0 0+2 0 0 0  +1 0 0 0 7 0 0 0   6 0 0 0 5 0 0 0   6 0 0 0 7 0 0 0
 3 0 0 0 0 0 0 0
'''
,
'''
 0 0 0 0 0 0 0 0   0 0 0 0 0 0 0 0   0 0 0 0 0 0 0 0   0 0 0 0 0 0 0 0
 0 0 0 0 0 0 0 0   0 0 0 0 0 0 0 0   0 0 0 0 0 0 0 0   0 0 0 0 0 0 0 0
 0 0 0 0 0 0 0 0   0 0 0 0 0 0 0 0   0 0 0 0 0 0 0 0   0 0 0 0 0 0 0 0
 0 0 0 0 0 0 0 0   0 0 0 0 0 0 0 0   0 0 0 0 0 0 0 0   0 0 0 0 0 0 0 0
 0 0 0 0 0 0 0 0   0 0 0 0 0 0 0 0   0 0 0 0 0 0 0 0   0 0 0 0 0 5 0 5
 0 5+2+2 0+3+3+3   0+1 0+1 0 3 0 0   0 0 0 0 0 0 0 0   0 0 6 0 0 7+1 5
 0 5+2+2 0+3+3+3   0+1 0+1 0 3 0 0   0 0 0 0 0 0 0 0   0 0 6 0 0 7+1 5
 0+4 0+4 7 7+2+4   0+2 0 4 6 4+1+1   0 7 0 4 4 4 6+1   0 7 0+1 6+1+3+5
 0+4 0+4 7 7+2+4   0+2 0 4 6 4+1+1   0 7 0 4 4 4 6+1   0 7 0+1 6+1+3+5
 0+2 0+1 7+2+2 7   0 7 0 2 4 2+1+1   0 7 0 4 4 4 6+1   0 7 0 6+1+1+1 7
 0 0 0 0 0 0 0 0   0 0 0 0 0 0 0 0   0 0 0 0 0 0 0 0   0 0 0 0 0 0 0 0
 0+4 0 0 0+3 0 0   0+2 0 0 0+2 0 0   0 7 0 0 0 6 0 0   0 7 0 6 5 7 0 0
 0+4 0 0 0+3 0 0   6+2 0 0 0+4 0 0   0+5 0 0 0+4 0 0  +5+6+4+5+6 0+1 5
 0 0+2+2 0+3+4+3   0+1 0+1 5+1+5*1  +6+4+4+2+2 7 7 5   5 5 4+1 6+1 5 5
 0 0 0 0 0 0 0 0   0 0 0 0 0 0 0 0   0 0 7+1+1+1+1+1   0 0 6+2 7 7+1 5
 0 0 0 0 0 0 0 0   0 0 0 0 0 0 0 0   0 0 7+1+1+1+1+1   0 0 6+2 7 7+1 5
 0 0 0 0 0 0 0 0   0 0 0 0 0 0 0 0   0 0 0 0 0 0 0 0   0 0 0 0 0 0 0 0
 0 0 0 0 0 0 0 0   0 0 0 0 0 0 0 0   0 0 0 0 0 0 0 0   0 0 0 0 0 0 0 0
 0 0 0 0 0 0 0 0
'''
,
'''
-1 0 0 0_5 0 0 0  _6 0 0 0_3 0 0 0  _4 0 0 0_5 0 0 0  _4 0 0 0_5 0 0 0
-1 0 0 0_5 0 0 0  _6 0 0 0_3 0 0 0  _4 0 0 0-1 0 0 0  _4 0 0 0_5 0 0 0
-1-5 1 3_7-2-5-7  _6-3-6 1_3-3-5-7  _4-1-4-6-1-3-5 1  _4-1-4-6_5-2-5-7
-1-3-5 1_5-2-5-7  _6-3-6 1_3-3-5-7  _4-1-4-6-1-3-5 1  _4-1-4-6_5-2-5-7
-1-3-5 1_5-2-5-7  _6-3-6 1_3-3-5-7  _4-1-4-6-1-3-5 1  _4-1-4-6_5-2-5-7
-1-3-5 1_7-2-5-7  _6-3-6 1_3-3-5-7  _4-1-4-6-1-3-5 1  _4-1-4-6_5-2-5-7
-1-3-5 1_5-2-5-7  _6-3-6 1_3-3-5-7  _4-1-4-6-1-3-5 1  _4-1-4-6_5-2-5-7
-1-5 1 0_5-2-7 0  _6-3 1 0_3-3-5 0  _4-1-6 0-1-5 1 0  _4-1-6 0_5-2-7 0
-1-5 1 0_5-2-7 0  _6-3 1 0_3-3-5 0  _4-1-6 0-1-5 1 0  _4-1-6 0_5-2-7 0
-1-5 1 0_5-2-7 0  _6-3 1 0_3-3-5 0  _4-1-6 0-1-5 1 0  _4-1-6 0_5-2-7 0
-1-5 1 3_5-2-5-7  _6-3-6 1_3-3-5-7  _4-1-4-6-1-5 1 3  _4-1-4-6_5-2-5-7
-1-3-5 3_5-2-5-7  _6-3-6 1_3-3-5-7  _4-1-4-6-1-5 1 3  _4-1-4-6_5-2-5-7
-1-3-5 3_5-2-5-7  _6-3-6 1_3-3-5-7  _4-1-4-6-1-5 1 3  _4-1-4-6_5-2-5-7
-1-3-5 3_5-2-5-7  _6-3-6 1_3-3-5-7  _4-1-4-6-1-5 1 3  _4-1-4-6_5-2-5-7
-1-3-5 3_5-2-5-7  _6-3-6 1_3-3-5-7  _4-1-4-6-1-5 1 3  _4-1-4-6_5-2-5-7
-1-3-5 3_5-2-5-7  _6-3-6 1_3-3-5-7  _4-1-4-6-1-5 1 3  _4-1-4-6_5-2-5-7
-1-3-5 1_7-2-5-7  _6-3-6 1_3-3-5-7  _4-1-4-6-1-3-5 1  _4-1-4-6_5-2-5-7
-1-3-5 1_7-2-5-7  _6-3-6 1_3-3-5-7  _4-1-4-6-1-3-5 1  _4-1-4-6_5-2-5-7
-1 0 0 0 0 0 0 0
'''
]

def waveFuncSinWithMask(time_seq, frequency, stride_time):
    mask = np.linspace(0, 1, time_seq.shape[0])
    mask = mask ** 0.5 # scale to left
    mask = 1 - ((mask - 0.5) ** 2) * 4
    wav = np.sin(2 * np.pi * frequency * time_seq) * mask
    return wav

def waveFuncElectricGuitar(time_seq, frequency, stride_time):
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

def logFrequencysToWave(log_frequencys, durations, base_frequency, base_amplitude, stride_time, framerate, wave_func):
    assert(len(log_frequencys) == len(durations))

    stride_length = int(framerate * stride_time)
    total_length = stride_length * (len(log_frequencys) - 1) + int(framerate * durations[-1])
    wav = np.zeros(total_length, dtype=np.float64)
    for i, log_frequency in enumerate(log_frequencys):
        if log_frequency is not None:
            start = i * stride_length
            frequency = base_frequency * (2 ** (log_frequency / 12))
            tune_length = int(durations[i] * framerate)
            time_seq = np.linspace(0, durations[i], tune_length)
            wav[start:start + tune_length] += wave_func(time_seq, frequency, stride_time) * base_amplitude
    return wav

BASE_FREQUENCY = 261.626
BASE_AMPLITUDE = 5000
STRIDE_TIME = 0.25
FRAMERATE = 44100

if 1: tune_map = {'1':0, '2':2, '3':4, '4':5, '5':7, '6':9, '7':11}
else: tune_map = {'1':0, '2':2, '3':3, '4':5, '5':7, '6':8, '7':10}

x1, x21, x22, x3 = [tuneToLogFrequency(tune_seq, tune_map) for tune_seq in canon_1_2_2_3]

def addBlank(seq):
    res = [None] * (len(seq) * 2)
    res[::2] = seq
    return res

def join(seq1, seq2):
    assert(len(seq1) == len(seq2))
    res = [None] * (len(seq1) * 2)
    res[::2] = seq1
    res[1::2] = seq2
    return res

log_frequencys_1_2_3 = [addBlank(x1), join(x21, x22), addBlank(x3)]
durations = [STRIDE_TIME * 3] * len(log_frequencys_1_2_3[0])

wavs = [logFrequencysToWave(log_frequencys, durations, BASE_FREQUENCY, BASE_AMPLITUDE, STRIDE_TIME, FRAMERATE
        , waveFuncElectricGuitar) for log_frequencys in log_frequencys_1_2_3]
wav = sum(wavs[1:], wavs[0])

assert(np.max(wav) < 32768)
assert(np.min(wav) >= -32768)
wav_short = wav.astype('<i2') # short

with wave.open("canon_electric_guitar.wav", 'wb') as wf:
    wf.setnchannels(1)
    wf.setframerate(FRAMERATE)
    wf.setsampwidth(2) # short
    wf.writeframes(wav_short.tobytes())
