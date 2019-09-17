import keras

class Language():
    def __init__(self, size):
        self.vocabSize = size

def build_model(Language):
    """ Returns structure of model for word vector optimization """
    vocabSize = Language.vocabSize
    initial_score_vec = keras.layers.Input(shape=(vocabSize,),
                                            name='initial_score_vec')
    dense_1 = keras.layers.Dense(units=vocabSize)(initial_score_vec)
    dense_2 = keras.layers.Dense(units=vocabSize)(dense_1)
    dense_3 = keras.layers.Dense(units=vocabSize)(dense_2)
    output = keras.layers.Dense(units=vocabSize, activation='relu')(dense_3)
    model = keras.models.Model(inputs=initial_score_vec,  outputs=output)
    return model

size = 5
e = Language(size)
m = build_model(e)
m.compile(optimizer='adam', loss='categorical_crossentropy')

import numpy as np

x = np.random.randint(low=0, high=10, size=(10000, size))
y = np.array([10*e for e in x])
print(x[0])
print(y[0])
m.fit(x, y, epochs=30)

import matplotlib.pyplot as plt

# while True:
# t = np.array([input(f'{i}: ') for i in range(size)])
t = np.expand_dims(np.array([0.1, 0.2, 0.3, 0.4, 0.5]), axis=0)
pred = (m.predict(t))
print(pred)
