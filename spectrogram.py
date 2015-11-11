import numpy as np
from pydub import *
import matplotlib.pyplot as plt

s = AudioSegment.from_mp3("Muramasa.mp3")
# s = AudioSegment.from_mp3("bloodmeat_drum.mp3")

y = s.get_array_of_samples()

time_frame = 1000*0.05

time_frame_slices = [s[i:i + time_frame ] for i in np.linspace(0, len(s)-time_frame, len(s)/time_frame ) ]

# take only the beginning
time_frame_slices = time_frame_slices[:int(len(time_frame_slices)*0.3)]

zs = []
print "number time_frame_slices ", len(time_frame_slices)
print "number of sample per time_frame ", len(time_frame_slices[0].get_array_of_samples())


downsample_value = 1

def downsample_array(a):
	if downsample_value == 1 :
		return a
	a = a[:(len(a)/downsample_value)*downsample_value]
	return a.reshape(len(a)/downsample_value, downsample_value).mean(axis=1)

for i, sl in enumerate(time_frame_slices):
	samples = sl.get_array_of_samples()
	sp = np.real(np.fft.fft(samples))
	down_freq = np.fft.fftfreq(len(samples), time_frame / 1000 /float(len(samples)) )
	positive_frequencies = (down_freq > 0 )
	down_logfreq = downsample_array(np.log10(down_freq[positive_frequencies]))
	down_sp = downsample_array(sp[positive_frequencies])
	zs.append(down_sp)


print 'done with ffts'
print down_logfreq

# x = [1, 2, 3, 4, 5]
# y = [0.1, 0.2, 0.3, 0.4, 0.5]

# intensity = [
#     [5, 10, 15, 20, 25],
#     [30, 35, 40, 45, 50],
#     [55, 60, 65, 70, 75],
#     [80, 85, 90, 95, 100],
#     [105, 110, 115, 120, 125]
# ]


# x, y = np.meshgrid(x, y)

# plt.pcolormesh(x, y, np.array(intensity).T)
# plt.colorbar()
# plt.show()


x, y = np.meshgrid(range(len(time_frame_slices)), down_logfreq)

plt.figure()
plt.pcolormesh(x, y, np.log10(np.absolute(np.array(zs).T)), cmap='Blues')
# plt.plot(range(len(y)), y)
plt.colorbar()
plt.show()
