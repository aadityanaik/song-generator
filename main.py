from song_preprocessing import Song
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense
import numpy as np


def create_sequences(data, seq_length):
    assert data, seq_length is not None
    x, y = [], []

    for i in range(int(len(data) / seq_length) - 1):
        seq = data[(i * seq_length): ((i + 1) * seq_length), 0]
        x.append(seq)
        y.append(data[(i + 1) * seq_length, 0])

    return np.array(x), np.array(y)


def generate_data(duration, originalSong):
    assert duration, originalSong is not None

    frame_rate = originalSong.framerate
    # duration is in milliseconds

    # TODO Add song generating algorithm... Will do later, cuz bored


song = Song(filename='Last Heroes - Dimensions [NCS Release].wav', format='wav')

song_data = np.array(song.data)

scaler = MinMaxScaler(feature_range=(-1, 1))
song_data = song_data.reshape(-1, 1)

scaled_data = scaler.fit_transform(song_data)

print(scaled_data.shape)

X, y = create_sequences(scaled_data, song.frame_rate)

X = np.reshape(X, (X.shape[0], 1, X.shape[1]))

print(X.shape, y.shape)

model = Sequential()
model.add(LSTM(64, input_shape=(1, song.frame_rate)))
model.add(Dense(1))
model.compile(loss='mean_squared_error', optimizer='rmsprop')

model.fit(X, y, epochs=100, batch_size=16)


'''
inverse_scaled_data = scaler.inverse_transform(scaled_data)

inverse_scaled_data = inverse_scaled_data.astype(np.int16)

other_song = Song(npArray=inverse_scaled_data, referenceSound=song)

other_song.save('diff_mlast_heroes.wav')
'''