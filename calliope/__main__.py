import time

from audio_input import AudioInput
from frequency_note_conversion import freq_to_note
from audio_grading import AudioGrading


tune_arr = [["C4"], ["R"], ["C4"], ["R"], ["C4"], ["C4"], ["C4"], ["C4"]]
bpm = 60

audio_grading = AudioGrading(tune_arr, bpm)
audio_grader = audio_grading.grade()
next(audio_grader)

for frequencies in AudioInput().start():
    print(audio_grader.send(frequencies))
    for frequency in frequencies:
        print(freq_to_note(frequency), end=" ")
    print()

print("done")