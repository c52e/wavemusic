import wave
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import pyaudio
import time

plt.style.use("dark_background")

class MusicAnimation(object):
    def __init__(self, filename, fps=20, yscale=0.1, max_freq_show=3000):
        wf = wave.open(filename) 
        assert(wf.getsampwidth() == 2)
        assert(wf.getnchannels() == 1)
        
        framerate = wf.getframerate()
        assert(framerate % fps == 0)

        chunk = framerate // fps
        
        self._len_show = int(max_freq_show / framerate * chunk)
        self._wav = np.frombuffer(wf.readframes(wf.getnframes()) , '<i2') / 32767
        self._max_freq_show = max_freq_show
        self._chunk = chunk
        self._wf = wf
        self._fps = fps
        self._yscale = yscale
    
    def _subplots(self):
        fig, ax = plt.subplots()
        ax.get_yaxis().set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        return fig, ax

    def _animateBase(self, i, ax):
        wav_show = self._wav[i * self._chunk: i * self._chunk + self._chunk]
        wav_freq = np.fft.fft(wav_show)
        wav_freq = np.abs(wav_freq) * 2
        #wav_freq = np.log(wav_freq)
        x = np.linspace(0, self._max_freq_show, self._len_show)
        y = wav_freq[:self._len_show]
        ax.clear()
        ax.plot(x, y)
        ax.set_ylim([0, self._chunk * self._yscale])

    def play(self):
        fig, ax = self._subplots()
        
        dt = 1 / self._fps
        def animate(i):
            self._animateBase(i, ax)
            while time.time() - start_time < dt * i:
                pass
        frames = self._wf.getnframes() // self._chunk
        ani = FuncAnimation(fig, animate, frames=frames, interval=0, repeat=False)

        wf = self._wf
        wf.rewind()
        p = pyaudio.PyAudio()
        stream = p.open(format = p.get_format_from_width(wf.getsampwidth()),
                        channels = wf.getnchannels(),
                        rate = wf.getframerate(),
                        output = True,
                        stream_callback=lambda in_data, frame_count, time_info, status: (wf.readframes(frame_count), pyaudio.paContinue))
        start_time = time.time()
        plt.show()
        stream.start_stream()
        while stream.is_active():
            pass
        stream.close()    
        p.terminate()

ani = MusicAnimation('canon_electric_guitar.wav')
ani.play()
