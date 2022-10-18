#!/usr/bin/env python
# coding: utf-8

# In[1]:


import tensorflow as tf
from tensorflow.keras.layers import Dense, Normalization, Input
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, TensorBoard

def autoencoder_dense(X_train,X_test,lr=0.001,pat=3,bat_size=64,epo=50):
    array = Input(shape=(256,))
    norm = Normalization()(array)
    x = Dense(128, activation="relu")(norm)
    x = Dense(64, activation="relu")(x)
    x = Dense(8, activation="relu")(x)
    x = Dense(64, activation="relu")(x)
    x = Dense(128, activation="relu")(x)
    decoded = Dense(256, activation="relu")(x)

    autoencoder = Model(array, decoded)
    autoencoder.compile(optimizer=Adam(learning_rate=lr),
                 loss='mean_squared_error')

    callback_conv = [EarlyStopping(monitor='val_loss', patience=pat),
                   TensorBoard(log_dir = "./logs/auto/{}-{}-{}-{}".format(datetime.datetime.today().month,
                                                                          datetime.datetime.today().day,
                                                                          datetime.datetime.today().hour,
                                                                          datetime.datetime.today().minute), update_freq="epoch")]
    history = autoencoder.fit(X_train, X_train,
          validation_data = (X_test, X_test),
                            batch_size=bat_size, 
                            epochs=epo, 
                            callbacks=[callback_conv])
    return autoencoder, history

