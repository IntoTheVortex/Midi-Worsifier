import sys
from mido import MidiFile, Message

#https://soundprogramming.net/file-formats/midi-note-frequencies/
NOTES = 'notes.txt'


#info:
'''https://stackoverflow.com/questions/50158890/attributeerror-module-midi-has-no-attribute-read-midifile
this link was needed to get the midi to work after pip install midi
change to this:
https://mido.readthedocs.io/en/latest/installing.html
'''



#https://www.personal.kent.edu/~sbirch/Music_Production/MP-II/MIDI/midi_file_format.htm
def read_midi(midi_file):
    #for python-midi:
    #pattern = midi.read_midifile(midi_file)
    #print(pattern)

    #ref https://mido.readthedocs.io/en/latest/midi_files.html
    #for mido:
    mid = MidiFile(midi_file)
    for i, track in enumerate(mid.tracks):
        print('Track {}: {}'.format(i, track.name))
        for msg in track:
            #print(msg)
            pass
    
class Midi_chart:
    def __init__(self):
        self.setup_notes()

        for i in range(len(self.notes)):
            print(i, self.notes[i])

    def setup_notes(self):
        notes = []
        n = open(NOTES)
        for line in n:
            notes.append(line)
        self.notes = [float(x) for x in notes]
        self.notes = [round(x) for x in self.notes]





def main():
    if len(sys.argv) < 2:
        print("Please enter a midi file as an argument.")
        sys.exit(1)
    midi_file = sys.argv[1]
    print(midi_file)
    read_midi(midi_file)
    chart = Midi_chart()





if __name__ == '__main__':
    main()