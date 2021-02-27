import json
import csv
from music21 import note, chord, stream, instrument
import numpy as np
from model import lstm_model

time_steps = 32

# load notes dict
with open('notes.json', 'r') as file:
    notes_dict = json.load(file)

############
# Load music data from csv produced by mid_to_csv.py
with open('mozart.csv', newline='') as file:
    reader = csv.reader(file)
    notes_array = list(reader)
    
notes_array = list(map(lambda x: x + [""], notes_array)) # empty string to represent the end
unique_notes = list(set(sum(notes_array ,[])))

max_length = np.max(list(map(lambda x: len(x), notes_array))) + 10

# save notes dict for prediction
with open('notes.json', 'w') as file:
    json.dump(notes_dict, file)

notes_array = [np.vectorize(notes_dict.get)(x) for x in notes_array]

x, y = [], []
for notes in notes_array:
    for i in range(0, len(notes) - time_steps, 1):
        
        # Preparing input and output sequences
        input = [[x] for x in notes[i:i + time_steps]]
        output = notes[i + time_steps]
        
        x.append(input)
        y.append(output)
        
x = np.array(x)
y = np.array(y)
#################

random_music = x[1]
# random_music = np.random.randint(1, len(notes_dict), size=(time_steps, 1))

model = lstm_model(len(notes_dict))
model.build((None, time_steps, 1))
model.summary()
model.load_weights('best_model.h5')

predictions = []
y_pred = 1

for i in range(100):

    prob = model.predict(random_music, batch_size=1)[0]
    y_pred = np.argmax(prob,axis=0)
    predictions.append(y_pred)

    if y_pred == 0:
        break

    random_music = np.concatenate((random_music[1:, :], [[y_pred]]), axis=0)
    

predictions = [list(notes_dict.keys())[i] for i in predictions]

def convert_to_midi(prediction_output):
   
    offset = 0
    output_notes = []

    # create note and chord objects based on the values generated by the model
    for pattern in prediction_output:
        
        # pattern is a chord
        if ('.' in pattern) or pattern.isdigit():
            notes_in_chord = pattern.split('.')
            notes = []
            for current_note in notes_in_chord:
                
                cn=int(current_note)
                new_note = note.Note(cn)
                new_note.storedInstrument = instrument.Piano()
                notes.append(new_note)
                
            new_chord = chord.Chord(notes)
            new_chord.offset = offset
            output_notes.append(new_chord)
            
        # pattern is a note
        else:
            
            new_note = note.Note(pattern)
            new_note.offset = offset
            new_note.storedInstrument = instrument.Piano()
            output_notes.append(new_note)

        # increase offset each iteration so that notes do not stack
        offset += 1
    midi_stream = stream.Stream(output_notes)
    midi_stream.write('midi', fp='music.mid')

convert_to_midi(predictions)