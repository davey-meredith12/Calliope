from audio_input import AudioInput
from frequency_note_conversion import freq_to_note

for frequencies in AudioInput().start():
    for frequency in frequencies:
        print(freq_to_note(frequency))
    print()
