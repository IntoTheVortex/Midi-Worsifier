**Midi Interpreter for Generated Music**

This project contains the code to translate midi files generated in the "Variations on a Theme - ML Music Generation" project.

Usage:
- Test the midi interpretation with the provided midi file:
    - `python midi_interpreter.py --midi=test_mag.mid --random=True`
    - the `--random` option will generate the file using random wave function generators from sine_by_freq.py
    - if the `--random` option is not used, the `--wave_style` option can specify "sine", "square", "sawtooth", "triangle", or "mod_1". The sine wave will be the default if neither wave_style or random are used.
    - the mod_1 wave generator is a glitchy triangle wave that has interesting properties
- Test the wave generators themselves by running:
    - `python sine_by_freq.py`
    - this will produce a file called melody.wav which contains tests of each wave generator


Notes:  
- In some midi files, the 'note_off' message type is not used. Instead, a 'note_on' message type with a velocity=0 is used to terminate the note. 
- This code only considers monophonic midi melodies, and will give unexpected results when using polyphonic midi files as input.
- Each midi track in a midi file is considered to be a separate and non-simultaneous melody and is interpreted as such.


**Report**

Originally, this project was intended to include a Magenta MelodyRNN trained on Blues melodies, to provide the midi files to translate into .wav files. However, the Magenta version that contains the models I wished to use has been deprecated, and the project was split into different parts and continued [here](https://magenta.tensorflow.org/). The version I used is hosted [here](https://github.com/magenta/magenta), and it requires some tinkering to get it set up properly in Windows (I now value Windows Subsystem for Linux very highly).

The partner project ["Variations on a Theme - ML Music Generation"](https://gitlab.cecs.pdx.edu/variations-on-a-theme/variations-on-a-theme-ml-music-generation) hosted on GitLab contains generated melodies created by the MelodyRNN trained on a Blues dataset.

Concerning the program contained in this project, the sine_by_freq.py program contains the five different waveform generators, which each generate rests as well as notes. The amplitude has been adjusted subjectively to sound relatively equal to each other. The write_mod_1 function was developed from a mistake in the write_triangle function that led to interesting output. Given more time, it would have been followed by mod_2, mod_3, etc., as other experiments in finding aurally interesting periodic functions.

Early in the project, attempting to create polyphonic sounds in a .wav format was abandoned in favor of focusing on monophonic sounds. This is another point of investigation for the future, and could be pursued using an interposition formula to allow for more than one note to play at a time.

The reading of the input midi file was aided by the mido library, though I discovered differences in the ways midi files are written that posed problems. Though the midi protocol contains both 'note_on' and 'note_off' types, in many cases, files are generated without the use of the 'note_off' type and simply use a 'note_on' type with the same note value as a previous note_on, and a velocity of 0. This is not immediately apparent, and it complicated the already-complicated timing issue. The timing for notes in midi files is relative to the last event, and is counted in 'ticks' instead of some more conventional time format. Eventually I found mido provided a method to convert time in ticks to time in seconds, and that worked well for monophonic midi files with no rests and with note_off message types. 

All three of those assumptions had to be addressed to result in the expected behavior. Since monophonic midi files are assumed, the program will handle any note overlap by cutting the first note short in order to play the next one. Rests were calculated using a flag to tell if a note was already playing, and if not, add up how much time had passed since the last note was played. Checks were added to detect whether the file was of the type that contained note_off messages or not, and called a different processing function in each case. 

Once all this information is read correctly, the midi note codes are converted into frequencies based on a read-in chart. Finally, the are sent to the sine_by_freq.py program to be written into a .wav file with the specified parameters.
