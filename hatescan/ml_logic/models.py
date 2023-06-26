# Import modules
import numpy as np
from tensorflow.keras import layers
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.layers import Embedding, Bidirectional, LSTM, Dense, Dropout, Masking
from tensorflow.keras.models import Sequential, layers, regularizers, optimizers
from tensorflow.keras.preprocessing.text import text_to_word_sequence

#MODEL_SCALE:
#Initialize and Compile MODEL_SCALE
def initialize_model_scale(vocab_size, embedding_dimension, learning_rate):
    l12 = regularizers.L1L2() #play with hyperparams
    model = Sequential()
    model.add(Embedding(input_dim=vocab_size + 1, output_dim=embedding_dimension, mask_zero=True))
    model.add(layers.Masking())
    model.add(Bidirectional(LSTM(32,  return_sequences=True, kernel_regularizer=l12)))
    model.add(Bidirectional(LSTM(16)))
    model.add(Dense(16, activation='relu', kernel_regularizer=l12))
    model.add(Dropout(0.5))
    model.add(Dense(3, activation='softmax'))

    optimizer = Adam(learning_rate=learning_rate)
    model.compile(loss='categorical_crossentropy', optimizer=optimizer , metrics=['Precision', 'Accuracy']) #precision because unbalanced dataset

    return model

# Fitting the MODEL_SCALE
def train_model_scale(
        model,
        X_train: np.ndarray,
        y_train: np.ndarray,
        batch_size=32,
        patience=5,
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
        class_weight = {0: 0.05, 1: 1.2, 2: 1} #more weight on class 1 & 2
    )

    return model, history

# Evaluating the MODEL_SCALE
def evaluate_model_scale(
        model,
        X: np.ndarray,
        y: np.ndarray,
        batch_size=64
    ):
    if model is None:
        print(f"\n❌ No model to evaluate")
        return None

    test_loss, test_precision, test_acc = model.evaluate(
        x=X,
        y=y,
        batch_size=batch_size,
        verbose=0,
        return_dict=True
    )

    print(f"✅ Model evaluated, Precision: {round(test_precision, 2)}")
    print(f"✅ Model evaluated, Accuracy: {round(test_acc, 2)}")

    return test_loss, test_precision, test_acc

#MODEL_TOPIC:
#Initialize and Compile MODEL_TOPIC
def initialize_model_topic(vocab_size, embedding_dimension, learning_rate):
    l12 = regularizers.L2() #play with hyperparams
    model = Sequential()
    model.add(Embedding(input_dim=vocab_size + 1, output_dim=embedding_dimension, mask_zero=True))
    model.add(layers.Masking())
    model.add(Bidirectional(LSTM(32,  return_sequences=True, kernel_regulizer=l12)))
    model.add(Bidirectional(LSTM(16)))
    model.add(Dense(16, activation='relu', kernel_reguralizer=l12))
    model.add(Dropout(0.5))
    model.add(Dense(5, activation='softmax'))

    optimizer = Adam(learning_rate=learning_rate)
    model.compile(loss='categorical_crossentropy', optimizer=optimizer , metrics=['Accuracy']) #precision because unbalanced dataset

    return model

# Fitting the MODEL_TOPIC
def train_model_topic(
        model,
        X_train: np.ndarray,
        y_train: np.ndarray,
        batch_size=32,
        patience=5,
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
        verbose=1
        )

    return model, history

# Evaluating the MODEL_TOPIC
def evaluate_model_topic(
        model,
        X: np.ndarray,
        y: np.ndarray,
        batch_size=64
    ):
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