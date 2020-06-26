import pyaudio
import struct
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

CHUNK = 1024 * 4
# samples per chunk

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100


p = pyaudio.PyAudio()

stream = p.open(
    format = FORMAT,
    channels= CHANNELS,
    rate = RATE,
    input= True,
    output = True,
    frames_per_buffer = CHUNK
)


#print(len(data)) # == 8192 = 2 * CHUNK

# add + 128 to re-reference to 0 rather than -127 (minimum)

# [::2] : this means to take every 2 points as sampling.




fig, ax = plt.subplots()
ax = plt.axes(ylim=(0,300), xlim=(0, CHUNK))

line, = ax.plot([],[], lw=2)

def init():
    line.set_data([], [])
    return line,


def animate(i):
    x = np.arange(0, 2 * CHUNK, 2)
    data = stream.read(CHUNK)
    data_int = np.array(struct.unpack(str(2 * CHUNK) + 'B', data), dtype='b')[::2]+128

    line.set_data(x, data_int)

    return line,


anim = animation.FuncAnimation(fig, animate, init_func=init,frames=200, interval=20, blit=True)

plt.show()


