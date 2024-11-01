import pyaudio
import wave
import time
import numpy
import scipy
import threading
import queue
import frequency_note_conversion

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 2048
OUTPUT_FILENAME = "recorded_audio.wav"
TIME_TO_RECORD = 2

def get_audio_input():
    # instantiate
    audio = pyaudio.PyAudio()
    # set up stream
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    # read incoming audio
    frames = []

    start_time = time.time()
    fft_queue = queue.Queue()
    finished_recording = False
    output_frequencies: queue.Queue = queue.Queue()

    # A function that will run on a thread that utilizes a queue to process data using fft.
    # All the frequencies will be put into the output_frequencies array
    def fft_thread():
        while not finished_recording or fft_queue.qsize() > 0:
            if fft_queue.qsize() > 0:
                N = CHUNK
                R = RATE

                queue_data = fft_queue.get()
                queue_data = numpy.frombuffer(queue_data, dtype=numpy.int16)

                # ignore if volume is too low
                if numpy.max(queue_data) < 400:
                    # print("Volume is to small: ", numpy.max(queue_data) )
                    continue

                fft_result = scipy.fft.fft(queue_data)
                # absolute value result to avoid imaginary numbers
                fft_result = numpy.abs(fft_result)
                # normalize result
                fft_max = numpy.max(fft_result)
                normalized_fft_result = fft_result / fft_max

                relative_maximums, _ = scipy.signal.find_peaks(normalized_fft_result, height=.7)
                # inverse of sample rate
                d = 1 / R
                frequencies = scipy.fft.fftfreq(N, d)
                maximum_frequencies = frequencies[relative_maximums]
                positive_maximum_frequencies = maximum_frequencies[maximum_frequencies > 0]
                # add output frequencies to the list
                output_frequencies.put(positive_maximum_frequencies)
                for frequency in positive_maximum_frequencies:
                        print(frequency_note_conversion.freq_to_note(frequency), end=" ")
                print("")
                #print(frequency_note_conversion.freq_to_note(positive_maximum_frequencies[0]))

    # start thread to begin processing data
    fft_thread = threading.Thread(target=fft_thread, args=[])
    fft_thread.start()

    # start recording
    while True:
        try:
            # perform fft here
            data = stream.read(CHUNK)
            frames.append(data)
            fft_queue.put(data)

        except Exception as e:
            print("Exception Occurred: ", e)
            break

        if time.time() - start_time >= TIME_TO_RECORD:
            break

    finished_recording = True
    fft_thread.join()

    # close up the stream
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # write to audio file
    wave_file = wave.open(OUTPUT_FILENAME, 'wb')
    wave_file.setnchannels(CHANNELS)
    wave_file.setsampwidth(audio.get_sample_size(FORMAT))
    wave_file.setframerate(RATE)
    wave_file.writeframes(b''.join(frames))
    wave_file.close()

if __name__ == '__main__':
    get_audio_input()

