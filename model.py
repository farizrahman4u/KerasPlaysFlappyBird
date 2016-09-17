from keras.layers import *
from keras.models import Sequential
import numpy as np
from keras.initializations import normal



model = Sequential()
model.add(Conv2D(32, 8, 8, subsample=(4, 4), input_shape=(4, 80, 80), init=lambda shape, name: normal(shape, scale=0.01, name=name), border_mode='same'))
model.add(Activation('relu'))
model.add(Conv2D(64, 4, 4, subsample=(2, 2), init=lambda shape, name: normal(shape, scale=0.01, name=name), border_mode='same'))
model.add(Activation('relu'))
model.add(Convolution2D(64, 3, 3, subsample=(1,1),init=lambda shape, name: normal(shape, scale=0.01, name=name), border_mode='same'))
model.add(Activation('relu'))
model.add(Flatten())
model.add(Dense(512, init=lambda shape, name: normal(shape, scale=0.01, name=name)))
model.add(Activation('relu'))
model.add(Dense(2,init=lambda shape, name: normal(shape, scale=0.01, name=name)))

model.compile(loss='mse', optimizer='adam')
