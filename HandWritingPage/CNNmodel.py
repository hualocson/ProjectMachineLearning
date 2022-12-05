import numpy as np
import pandas as pd
from tensorflow import keras
from sklearn.model_selection import train_test_split
from keras.utils.np_utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D, BatchNormalization
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import LearningRateScheduler, ReduceLROnPlateau, ModelCheckpoint
from tensorflow.keras.optimizers import RMSprop

IMAGE_SIZE = (12, 28)
BATCH_SIZE = 128
EPOCHS = 50
WEIGHT_INIT = 0.05
WEIGHT_DECAY = 1e-4

ALPHA_DICT = {'0' : 0, '1' : 1, '2' : 2, '3' : 3, '4' : 4, '5' : 5, '6' : 6, '7' : 7, '8' : 8, '9' : 9, '10' : 10, 'A' : 11, 'B' : 12, 'C' : 13,
            'D': 14, 'E': 15, 'F': 16, 'G': 17, 'H': 18, 'K': 19, 'L': 20, 'M': 21, 'N': 22, 'P': 23, 'R' : 24, 'S' : 25, 'T' : 26,
            'U' : 27, 'V' : 28, 'X' : 29, 'Y' : 30, 'Z' : 31}
class CNN_Model(object):
    def __init__(self, trainable=True):
        self.batch_size = BATCH_SIZE
        self.trainable = trainable
        self.num_epochs = EPOCHS
        # Building model
        self._build_model()

        # Input data
        if trainable:
            self.model.summary()
            self.data = train
            self.y = y_train

        optimizer = RMSprop(learning_rate=0.001, rho=0.9, epsilon=1e-08)
        self.model.compile(loss="sparse_categorical_crossentropy", optimizer=optimizer, metrics=['acc'])

    def _build_model(self):
        # CNN model
        self.model = Sequential()
        self.model.add(Conv2D(32, (5, 5), padding='same', activation='relu', input_shape=(28, 12, 3)))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))
        self.model.add(Conv2D(32, (5, 5), activation='relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))
        self.model.add(Flatten())
        self.model.add(Dense(512, activation='relu'))
        self.model.add(Dropout(0.25))
        self.model.add(Dense(32, activation='softmax'))

    def train(self):
        learning_rate_reduction = ReduceLROnPlateau(monitor='acc',
                                            patience=3,
                                            verbose=1,
                                            factor=0.5,
                                            min_lr=0.00001)

        print("Training......")
        trainX = self.data
        trainY = self.y
        trainX = np.array(trainX)
        trainY = np.array(trainY)

        self.model.fit(datagen.flow(trainX, trainY, batch_size=self.batch_size), callbacks=[learning_rate_reduction], verbose=1,
                       epochs=self.num_epochs, shuffle=True)
        # Save model
        self.model.save(r'mymodel.h5')

    def predict(self):
        testX = test
        testX = np.array(testX)
        testY = np.argmax(self.model.predict(testX), axis=1)
        testY = np.array(testY)
        print("Predicting... ")
        print(testY)

    def test_pic(self, pic):
        testX = pic
        testX = np.array(testX)
        testY = np.argmax(self.model.predict(testX), axis=1)
        testY = np.array(testY)
        keys = list(ALPHA_DICT.keys())
        return str(keys[testY[0]])

    def load(self, model_name):
        self.model = keras.models.load_model(model_name)
        self.model.summary()
