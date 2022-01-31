import struct
import sys
import wave
from functools import lru_cache
import numpy as np
from waves import *

def BinaryStream(filename: str):
    file = open(filename, 'rb')
    def read(format: str):
        size = struct.calcsize(format)
        binary = file.read(size)
        return struct.unpack(format, binary)
    return read

def read_var_len(stream):
    value = 0
    while True:
        byte, = stream('B')
        value = ((value << 7) | (byte & 0x7f))
        if (byte & 0x80) == 0:
            break
    return value

def read_uint24(stream):
    high, low = stream('>BH')
    return (high << 16) | low

def read_midi(filename):
    stream = BinaryStream(filename)

    # ref: https://www.music.mcgill.ca/~ich/classes/mumt306/StandardMIDIfileformat.html
    #      https://github.com/colxi/midi-parser-js/wiki/MIDI-File-Format-Specifications
    # Incomplete version
    chunk_type, length, format, ntrks, division = stream('>4sI3H')
    assert chunk_type == b'MThd'
    assert length == 6
    assert format in [0,1]
    assert ntrks == 1
    assert (division & 0x8000) == 0

    chunk_type, length = stream('>4sI')
    assert chunk_type == b'MTrk'

    delta_time = read_var_len(stream)
    assert delta_time == 0
    event_type, = stream('B')
    assert event_type == 0xff
    meta_event_type, = stream('B')
    assert meta_event_type == 0x03
    length = read_var_len(stream)
    track_name, = stream(f'{length}s')
    print(f'Track Name: {track_name.decode("utf-8")}')

    delta_time = read_var_len(stream)
    assert delta_time == 0
    event_type, = stream('B')
    assert event_type == 0xff
    meta_event_type, = stream('B')
    assert meta_event_type == 0x51
    length = read_var_len(stream)
    assert length == 3
    tempo = read_uint24(stream)
    print(f'BPM: {60000000 / tempo}')

    tick = 0
    ticks = []
    keys = []
    while True:
        delta_time = read_var_len(stream)
        tick += delta_time
        event_type, = stream('B')
        if event_type == 0x80:
            key, velocity = stream('BB')
        elif event_type == 0x90:
            key, velocity = stream('BB')
            ticks.append(tick)
            keys.append(key)
        elif event_type == 0xff:
            meta_event_type, = stream('B')
            assert meta_event_type == 0x2f
            length = read_var_len(stream)
            assert length == 0
            break
        else:
            raise Exception(f'Yet unknown event type: {event_type}')
    return division, tempo, ticks, keys

def main(args):
    assert len(args) == 2
    midi_path = args[1]
    assert midi_path[-4:] == '.mid'
    wav_path = f"{midi_path[:-4]}.wav"

    division, tempo, ticks, keys = read_midi(midi_path)
    seconds_per_tick = 1e-6 * tempo / division
    times = [tick * seconds_per_tick for tick in ticks]
    freqs = [(2.0 ** ((key - 69) / 12.0)) * 440 for key in keys]

    BASE_AMPLITUDE = 5000
    FRAMERATE = 44100
    STRIDE = 0.25
    NOTE_DURATION = 4.0

    note_length = int(FRAMERATE * NOTE_DURATION)
    wav = np.zeros(int(max(times) * FRAMERATE) + note_length)
    time_seq = np.linspace(0, NOTE_DURATION, note_length)

    wave_func = lru_cache()(lambda freq: waveKalimba(time_seq, freq, STRIDE) * BASE_AMPLITUDE)

    for time, freq in zip(times, freqs):
        i = int(time * FRAMERATE)
        wav[i:i+note_length] += wave_func(freq)

    assert np.max(wav) < 32768
    assert np.min(wav) >= -32768
    wav_short = wav.astype('<i2') # short
    with wave.open(wav_path, 'wb') as wf:
        wf.setnchannels(1)
        wf.setframerate(FRAMERATE)
        wf.setsampwidth(2) # short
        wf.writeframes(wav_short.tobytes())
    print('Output:', wav_path)

if __name__ == '__main__':
    main(sys.argv)
