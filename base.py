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
