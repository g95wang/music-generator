import numpy as np
from music21 import converter, note, chord, instrument
import os

#defining function to read MIDI files
def read_midi(file):
    
    print("Loading Music File:",file)
    
    notes, durations = [], []
    notes_to_parse = None
    
    #parsing a midi file
    midi = converter.parse(file)
  
    #grouping based on different instruments
    s2 = instrument.partitionByInstrument(midi)

    #Looping over all the instruments
    for part in s2.parts:
    
        #select elements of only piano
        if 'Piano' in str(part): 
        
            notes_to_parse = part.recurse() 
      
            #finding whether a particular element is note or a chord
            for element in notes_to_parse:
                
                #note
                if isinstance(element, note.Note):
                    notes.append(str(element.pitch))
                    durations.append(str(element.quarterLength))
                
                #chord
                elif isinstance(element, chord.Chord):
                    notes.append('.'.join(str(n) for n in element.normalOrder))
                    durations.append(str(element.quarterLength))

    return ','.join(notes), ','.join(durations)


path = 'data/raw/'
files = [file for file in os.listdir(path) if file.endswith(".mid")]

notes_array, durations_array = [], []
for file in files:
    notes, durations = read_midi(path + file)
    notes_array.append(notes)
    durations_array.append(durations)

np.savetxt('data/notes.csv', notes_array, delimiter=',', fmt='%s')
np.savetxt('data/duration.csv', durations_array, delimiter=',', fmt='%s')