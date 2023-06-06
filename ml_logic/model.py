# Import modules
import numpy as np

# Import initialize model
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import layers
from tensorflow.keras.callbacks import EarlyStopping


from tensorflow.keras.layers import Embedding, Bidirectional, LSTM, Dense, Dropout
from tensorflow.keras.models import Sequential, layers, regularizers, optimizers




# Initialize the model
def initialize_model():

    model = Sequential()
    model.add(Bidirectional(LSTM(64,  return_sequences=True)))
    model.add(Bidirectional(LSTM(32)))
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(3, activation='softmax'))

    return model

# Compiling the model
def compile_model(model):

    # we can add the optimizer=Adam(lr=0.5)) # vhigh lr so we can converge a little with such a small dataset

    model.compile(loss='categorical_crossentropy', optimizers='adam', metrics=['accuracy'])

    # Example compile
    # model.compile(loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
    #           optimizer=tf.keras.optimizers.Adam(1e-4),
    #           metrics=['accuracy'])

    return model

# Fitting the model
def train_model(


    model.fit(X_train, y_train,
          epochs=20,
          batch_size=32,
          validation_split=0.3,
          callbacks=[es]

    es = EarlyStopping(
        monitor="val_loss",
        patience=5,
        restore_best_weights=True,
        verbose=1
    )

    es = EarlyStopping(patience=5, restore_best_weights=True)


    history = model.fit(
        X,
        y,
        validation_data=validation_data,
        validation_split=validation_split,
        epochs=100,
        batch_size=batch_size,
        callbacks=[es],
        verbose=0
    )

    print(f"✅ Model trained on {len(X)} rows with min val MAE: {round(np.min(history.history['val_mae']), 2)}")

    return model, history

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
