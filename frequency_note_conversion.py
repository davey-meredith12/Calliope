import numpy

def freq_to_note(frequency):
    if frequency <= 0:
        return
    print("frequency being input ", frequency)
    #key number = 12 log_2 (f/440) + 49:
    key_number = round(12 * numpy.log2(frequency/440)+49)
    note_dict = {
        0: "G#",
        1: "A",
        2: "A#",
        3: "B",
        4: "C",
        5: "C#",
        6: "D",
        7: "D#",
        8: "E",
        9: "F",
        10: "F#",
        11: "G"
    }
    note_name = note_dict[(key_number % 12)]
    if (key_number % 12) - 1 < 3:
        note_number = (key_number // 12)
    else:
        note_number = (key_number // 12) + 1
    note = note_name + str(note_number)
    return note