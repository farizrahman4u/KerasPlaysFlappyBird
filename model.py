from keras.layers import *
from keras.models import Sequential

model = Sequential()
model.add(Conv2D(32, 8, 8, subsample=(4, 4), input_shape=(4, 80, 80)))
model.add(MaxPooling2D())
model.add(Conv2D(64, 4, 4, subsample=(2, 2)))
#model.add(MaxPooling2D())
#model.add(Conv2D(64, 3, 3))
#model.add(MaxPooling2D())
model.add(Flatten())
model.add(Activation('relu'))
model.add(Dense(2))
'''

model = Sequential()
model.add(Flatten(input_shape=(4, 80, 80)))
model.add(Dense(100))
model.add(Activation('relu'))
model.add(Dense(100))
model.add(Activation('relu'))
model.add(Dense(2))
'''
model.compile(loss='mse', optimizer='adam')
