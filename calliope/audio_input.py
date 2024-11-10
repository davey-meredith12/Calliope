import pyaudio
import time
import numpy
import scipy
import threading
import queue

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 2048
OUTPUT_FILENAME = "recorded_audio.wav"
TIME_TO_RECORD = 10

class AudioInput:
    _stream_thread: threading.Thread
    _decode_thread: threading.Thread
    _stream_queue: queue.Queue
    _decode_queue: queue.Queue
    _running: bool

    def __init__(self):
        self._stream_thread = threading.Thread(target=self._stream, args=[])
        self._decode_thread = threading.Thread(target=self._decode, args=[])
        self._stream_queue = queue.Queue()
        self._decode_queue = queue.Queue()

    def start(self):
        self._stream_thread.start()
        self._decode_thread.start()

    def stop(self):
        self._stream_thread.join()
        # close up the stream

    def _stream(self):
        # set up stream
        print("Input stream starting!")
        start_time = time.time()
        audio = pyaudio.PyAudio()
        stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
        while time.time() - start_time < TIME_TO_RECORD:
            try:
                self._stream_queue.put(stream.read(CHUNK))
            except Exception as e:
                print("Exception Occurred: ", e)
                break
        # close down input stream
        stream.stop_stream()
        stream.close()
        audio.terminate()
        print("Input stream exiting!")

    def _decode(self):
        print("Decode stream starting!")
        while self._stream_thread.is_alive():
            try:
                buffer = self._stream_queue.get(timeout=1)
                array = numpy.frombuffer(buffer, dtype=numpy.int16)
                if numpy.max(array) < 400:
                    # Not enough information to process
                    continue

                fft_result = scipy.fft.fft(array)
                # absolute value result to avoid imaginary numbers
                fft_result = numpy.abs(fft_result)
                # normalize result
                fft_max = numpy.max(fft_result)
                normalized_fft_result = fft_result / fft_max

                relative_maximums, _ = scipy.signal.find_peaks(normalized_fft_result, height=.7)
                # inverse of sample rate
                d = 1 / RATE
                frequencies = scipy.fft.fftfreq(CHUNK, d)
                maximum_frequencies = frequencies[relative_maximums]
                yield maximum_frequencies[maximum_frequencies > 0]
            except queue.Empty:
                # If the queue is empty, cycle to see if thread is still active
                continue
