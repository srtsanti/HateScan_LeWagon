# Import modules
import numpy as np

from tensorflow.keras import layers
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping

from keras import Model, Sequential, layers, regularizers, optimizers
from tensorflow.keras.preprocessing.text import text_to_word_sequence
from tensorflow.keras.preprocessing.text import text_to_word_sequence

#import and initialize model

def initialize_model(vocab_size, embedding_dimension):
    l2 = regularizers.l2() #play with hyperparams
    model = Sequential()
    model.add(layers.Embedding(input_dim=vocab_size + 1, output_dim=embedding_dimension, mask_zero=True))
    model.add(layers.Masking())
    model.add(layers.Bidirectional(layers.LSTM(64,  return_sequences=True)))
    model.add(layers.Bidirectional(layers.LSTM(32)))
    model.add(layers.Dense(64, activation='relu', kernel_regularizer=l2)) #add l2 regula
    model.add(layers.Dropout(0.5))
    model.add(layers.Dense(3, activation='softmax'))

    return model

# Compiling the model
def compile_model(model, learning_rate):

    optimizer = Adam(learning_rate=learning_rate)
    model.compile(loss='categorical_crossentropy', optimizer=optimizer , metrics=['accuracy'])

    return model

# Fitting the model
def train_model(
        model,
        X_train: np.ndarray,
        y_train: np.ndarray,
        batch_size=32,
        patience=2,
        validation_split=0.2
    ):

    es = EarlyStopping(
        monitor="val_loss",
        patience=patience,
        restore_best_weights=True)

    history = model.fit(
        X_train,
        y_train,
        validation_split=validation_split,
        epochs=100,
        batch_size=batch_size,
        callbacks=[es],
        verbose=1,
        class_weight = {0: 0.1, 1: 0.2, 2: 10000}
    )

    return model, history

# Evaluating the model
def evaluate_model(
        model,
        X: np.ndarray,
        y: np.ndarray,
        batch_size=64
    ):
    """
    Evaluate trained model performance on the dataset
    """

    if model is None:
        print(f"\n❌ No model to evaluate")
        return None

    test_loss, test_acc = model.evaluate(
        x=X,
        y=y,
        batch_size=batch_size,
        verbose=0,
        return_dict=True
    )

    print(f"✅ Model evaluated, Accuracy: {round(test_acc, 2)}")

    return test_loss, test_acc

# Making predictions fromt the model
def model_predict(model,
                  X_new: np.array):

    predictions = model.predict(X_new)
    print(predictions)
