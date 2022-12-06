#!/usr/bin/env python
# coding: utf-8

# In[1]:

import datetime
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.layers import Dense, Normalization, Input
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, TensorBoard

def autoencoder_dense(X,Y,X_val,Y_val,lr=0.001,pat=5,bat_size=128,epo=100,inshape=256,bn=16):
	array = Input(shape=(256,))
	norm = Normalization()(array)
	x = Dense(128, activation="relu")(norm)
	x = Dense(64, activation="relu")(x)
	x = Dense(bn, activation="relu")(x)
	x = Dense(64, activation="relu")(x)
	x = Dense(128, activation="relu")(x)
	decoded = Dense(inshape, activation="relu")(x)

	autoencoder = Model(array, decoded)
	autoencoder.compile(optimizer=Adam(learning_rate=lr),
		loss='mean_squared_error')

	callback_conv = [EarlyStopping(monitor='val_loss', patience=pat),
		TensorBoard(log_dir = "./logs/auto/{}-{}-{}-						{}".format(datetime.datetime.today().month,
		datetime.datetime.today().day,
		datetime.datetime.today().hour,
		datetime.datetime.today().minute), update_freq="epoch")]
	history = autoencoder.fit(X, Y,
		validation_data = (X_val, Y_val),
		batch_size=bat_size, 
		epochs=epo, 
		callbacks=[callback_conv],verbose=0)
	loss = history.history['loss']
	val_loss = history.history['val_loss']


	plt.plot(loss, label='Training Loss')
	plt.plot(val_loss, label='Validation Loss')
	plt.legend(loc='upper right')
	plt.ylabel('Cross Entropy')
	plt.title('Training and Validation Loss')
	plt.xlabel('epoch')
	plt.yscale("log")
	plt.show()
	return autoencoder

