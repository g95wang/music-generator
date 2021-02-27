import numpy as np
import csv
import json
from model import lstm_model, cnn_model
from sklearn.model_selection import train_test_split
from tensorflow.keras.callbacks import ModelCheckpoint

time_steps = 32

# Load music data from csv produced by mid_to_csv.py
with open('mozart.csv', newline='') as file:
    reader = csv.reader(file)
    notes_array = list(reader)
    
notes_array = list(map(lambda x: x + [""], notes_array)) # empty string to represent the end
unique_notes = list(set(sum(notes_array ,[])))

max_length = np.max(list(map(lambda x: len(x), notes_array))) + 10
notes_dict = dict(zip(unique_notes, list(range(len(unique_notes)))))

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


model = lstm_model(len(unique_notes))
model.build((None, time_steps, 1))
model.summary()

print(x.shape)

saveCheckpoint = ModelCheckpoint('best_model.h5', monitor='val_loss', mode='min', save_best_only=True, verbose=1)
history = model.fit(x, y, validation_split=0.2, batch_size=64, epochs=50, steps_per_epoch=100, callbacks=[saveCheckpoint])