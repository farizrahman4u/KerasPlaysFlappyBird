from keras.layers import *
from keras.models import Sequential
import numpy as np


model = Sequential()
model.add(Conv2D(32, 8, 8, subsample=(4, 4), input_shape=(1, 80, 80)))
model.add(MaxPooling2D())
model.add(Activation('relu'))
model.add(Conv2D(64, 4, 4, subsample=(2, 2)))
model.add(MaxPooling2D())
model.add(Flatten())
model.add(Activation('relu'))
model.add(Dense(128))
model.add(Activation('relu'))
model.add(Dense(2))

model.compile(loss='mse', optimizer='adam')
