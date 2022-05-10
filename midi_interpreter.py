import sys
import midi



#info:
'''https://stackoverflow.com/questions/50158890/attributeerror-module-midi-has-no-attribute-read-midifile
this link was needed to get the midi to work after pip install midi
'''



#https://www.personal.kent.edu/~sbirch/Music_Production/MP-II/MIDI/midi_file_format.htm
def read_midi(midi_file):
    pattern = midi.read_midifile(midi_file)
    print(pattern)




def main():
    if len(sys.argv) < 2:
        print("Please enter a midi file as an argument.")
        sys.exit(1)
    midi_file = sys.argv[1]
    print(midi_file)
    read_midi(midi_file)





if __name__ == '__main__':
    main()