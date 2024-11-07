import time
import numpy as np

#currently written for quarter notes
simple_tune = [["A4"], ["R"], ["A4"], ["R"]]

correct_notes = [[440],[0],[440],[0]]
BPM = 60
FREQ_DIFF_ALLOWED = 1
#correct notes and correct timing length will be the same

def notes_arr_to_freq_arr(notes):
    freq_arr = []




#compared one at a time against the correct_notes
#Must be called timed based on the beat
def compare(input: list[float], time_since_start: float):
    arr_loc = round(time_since_start/(BPM/60))
    print("looking at " , arr_loc)
    print("comparing ", input, " against ", correct_notes[arr_loc])
    #compare arrays with tolerance of values
    return np.isclose(input, correct_notes[arr_loc], atol = FREQ_DIFF_ALLOWED)

if __name__ == '__main__':
    user_input = [[440.3], [0], [441], [0]]
    for i in range(4):
        timeToSleep = 1
        time.sleep(timeToSleep)
        timing = i * timeToSleep
        print(compare(user_input[i], timing))