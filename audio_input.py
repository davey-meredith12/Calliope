import pyaudio
import wave
import time

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
OUTPUT_FILENAME = "recorded_audio.wav"

#instantiate
audio = pyaudio.PyAudio()
#set up stream
stream = audio.open(format = FORMAT, channels = CHANNELS, rate = RATE, input = True, frames_per_buffer = CHUNK)
#read incoming audio
frames = []

start_time = time.time()

while True:
    try:
        data = stream.read(CHUNK)
        frames.append(data)
    except:
        break
    if time.time() - start_time >= 5:
        break

#close up the stream
stream.stop_stream()
stream.close()
audio.terminate()

#write to audio file
waveFile = wave.open(OUTPUT_FILENAME, 'wb')
waveFile.setnchannels(CHANNELS)
waveFile.setsampwidth(audio.get_sample_size(FORMAT))
waveFile.setframerate(RATE)
waveFile.writeframes(b''.join(frames))
waveFile.close()
