import sys






def read_midi(midi_file):
    pass




def main():
    if len(sys.argv) < 2:
        print("Please enter a midi file as an argument.")
        sys.exit(1)
    midi_file = sys.argv[1]
    print(midi_file)
    read_midi(midi_file)





if __name__ == '__main__':
    main()