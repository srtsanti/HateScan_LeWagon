# Import modules
import numpy as np

from tensorflow import keras
from tensorflow.keras.optimizers import Adam

from tensorflow.keras.layers import Embedding, Bidirectional, LSTM, Dense, Dropout
from keras import Model, Sequential, layers, regularizers, optimizers



# Initialize the model
def initialize_model(input_shape: tuple) -> Model:

    model = Sequential(shape=input_shape)
    model.add(layers.Input(shape=input_shape))
    model.add(layers.B )


    encoder,
    tf.keras.layers.Embedding(len(encoder.get_vocabulary()), 64, mask_zero=True),
    tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64,  return_sequences=True)),
    tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(32)),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(1, activation)
    ])
    return model


def initialize_model(input_shape: tuple) -> Model:
    """
    Initialize the Neural Network with random weights
    """
    reg = regularizers.l1_l2(l2=0.005)

    model = Sequential()
    model.add(layers.Input(shape=input_shape))
    model.add(layers.Dense(100, activation="relu", kernel_regularizer=reg))
    model.add(layers.BatchNormalization(momentum=0.9))
    model.add(layers.Dropout(rate=0.1))
    model.add(layers.Dense(50, activation="relu"))
    model.add(layers.BatchNormalization(momentum=0.9))  # use momentum=0 to only use statistic of the last seen minibatch in inference mode ("short memory"). Use 1 to average statistics of all seen batch during training histories.
    model.add(layers.Dropout(rate=0.1))
    model.add(layers.Dense(1, activation="linear"))

    print("✅ Model initialized")

    return model

# Compiling the model
def compile_model():
    model.compile(loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
              optimizer=tf.keras.optimizers.Adam(1e-4),
              metrics=['accuracy'])

    return model

# Fitting the model
def fit_model():
    history = model.fit(train_dataset, epochs=10,
                    validation_data=test_dataset,
                    validation_steps=30)

# Evaluating the model
def evaluate_model():
    test_loss, test_acc = model.evaluate(test_dataset)

    print('Test Loss:', test_loss)
    print('Test Accuracy:', test_acc)

# Making predictions fromt the model
def model_predict():
    # predict on a sample text without padding.

    sample_text = ('The movie was not good. The animation and the graphics '
                'were terrible. I would not recommend this movie.')
    predictions = model.predict(np.array([sample_text]))
    print(predictions)
