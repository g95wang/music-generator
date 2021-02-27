import tensorflow
from tensorflow.keras import Sequential
from tensorflow.keras.layers import LSTM, Dense, Embedding, Conv1D, MaxPool1D, GlobalMaxPool1D, Dropout

def lstm_model(n_notes):
    model = Sequential()
    model.add(Embedding(n_notes, 64))
    model.add(LSTM(128,return_sequences=True))
    model.add(LSTM(128))
    model.add(Dense(256, activation='relu'))
    model.add(Dense(n_notes, activation='softmax'))
    model.compile(loss='sparse_categorical_crossentropy', optimizer='adam')
    return model

def cnn_model(n_notes):
    model = Sequential()
        
    #embedding layer
    model.add(Embedding(len(n_notes), 100, input_length=32, trainable=True)) 

    model.add(Conv1D(64,3, padding='causal',activation='relu'))
    model.add(Dropout(0.2))
    model.add(MaxPool1D(2))
        
    model.add(Conv1D(128,3,activation='relu',dilation_rate=2,padding='causal'))
    model.add(Dropout(0.2))
    model.add(MaxPool1D(2))

    model.add(Conv1D(256,3,activation='relu',dilation_rate=4,padding='causal'))
    model.add(Dropout(0.2))
    model.add(MaxPool1D(2))
            
    #model.add(Conv1D(256,5,activation='relu'))    
    model.add(GlobalMaxPool1D())
        
    model.add(Dense(256, activation='relu'))
    model.add(Dense(len(n_notes), activation='softmax'))
        
    model.compile(loss='sparse_categorical_crossentropy', optimizer='adam')
    return model
