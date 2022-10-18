#!/usr/bin/env python
# coding: utf-8

# In[1]:


def conv1d(X_train,X_test,y_train,y_test,lr=0.001,pat=3,bat_size=64,epo=50):
    array = Input(shape=(256,))
    x = Conv1D(256, 5, padding='same', activation='relu', input_shape=(np.shape(X_pred)[1], 1))(array)
    x = Flatten()(x)
    x = Dense(64,activation='relu')
    x = Dense(32,activation='relu')
    x = Dense(8,activation='relu')
    x = Dense(1, activation='sigmoid')

    autoencoder = Model(array, x)
    autoencoder.compile(optimizer=Adam(learning_rate=lr),
                        loss='binary_crossentropy',
                        metrics=['accuracy'])

    conv_callback = [EarlyStopping(monitor='val_loss', patience=10),
               TensorBoard(log_dir = "./logs/conv/{}-{}-{}-{}".format(datetime.datetime.today().month,
                                                                      datetime.datetime.today().day,
                                                                      datetime.datetime.today().hour,
                                                                      datetime.datetime.today().minute), update_freq="epoch")
]
    history = autoencoder.fit(X_train, y_train,
          validation_data = (X_test, y_test),
                            batch_size=bat_size, 
                            epochs=epo, 
                            callbacks=[callback_conv])
    return conv1d_model, history_conv1d

