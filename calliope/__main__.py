import time

from audio_input import AudioInput
from frequency_note_conversion import freq_to_note, note_to_freq
from audio_grading import AudioGrading


tune_arr = [["C4"], ["R"], ["C4"], ["R"], ["C4"], ["C4"], ["C4"], ["C4"]]
bpm = 60

print("C4 is ", note_to_freq("C4"))
print(261.6255653005986, " is C4")

audio_grading = AudioGrading(tune_arr, bpm)
audio_grader = audio_grading.grade()
next(audio_grader)

prev_time = time.time()
for frequencies in AudioInput().start():
    if time.time() - prev_time >= 1:
        print("Input frequencies ", frequencies, " ", freq_to_note(frequencies[0]))
        print("Bool results " , audio_grader.send(frequencies))
        print()
        prev_time = time.time()
    #for frequency in frequencies:
        #print(freq_to_note(frequency), end=" ")
    #print()

# print(audio_grading.get_final_grade())
print("done")