import sounddevice
from scipy.io.wavfile import write

print('Recording...')

fs=44100
second=5

record = sounddevice.rec(int(second * fs), samplerate=fs, channels=2)

sounddevice.wait()

write("output.wav", fs, record)

print('Done recording!')