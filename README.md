**Midi Interpreter for Generated Music**

This project contains the code to translate midi files generated in the "Variations on a Theme - ML Music Generation" project.

Usage:
- Test the midi interpretation with the provided midi file:
    - python midi_interpreter.py --midi=test_mag.mid --random=True
    - the --random option will generate the file using random wave function generators from sine_by_freq.py
    - if the --random option is not used, the --wave_style option can specify "sine", "square", "sawtooth", "triangle", or "mod_1". The sine wave will be the default if neither wave_style or random are used.
    - the mod_1 wave generator is a glitchy triangle wave that has interesting properties
- Test the wave generators themselves by running:
    - python sine_by_freq.py
    - this will produce a file called melody.wav which contains tests of each wave generator


Notes:  
- In some midi files, the 'note_off' message type is not used. Instead, a 'note_on' message type with a velocity=0 is used to terminate the note. 
- This code only considers monophonic midi melodies, and will give unexpected results when using polyphonic midi files as input.
- Each midi track in a midi file is considered to be a separate and non-simultaneous melody and is interpreted as such.
