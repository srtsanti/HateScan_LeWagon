# Import modules
import numpy as np

# Import initialize model
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import layers
from tensorflow.keras.callbacks import EarlyStopping


from tensorflow.keras.layers import Embedding, Bidirectional, LSTM, Dense, Dropout, Masking
from tensorflow.keras.models import Sequential, layers, regularizers, optimizers
from tensorflow.keras.preprocessing.text import text_to_word_sequence


def initialize_model():

    model = Sequential()
    model.add(layers.Masking())
    model.add(Bidirectional(LSTM(64,  return_sequences=True)))
    model.add(Bidirectional(LSTM(32)))
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(3, activation='softmax'))

    return model

# Compiling the model
def compile_model(model, learning_rate):

    # we can add the optimizer=Adam(lr=0.5)) # vhigh lr so we can converge a little with such a small dataset
    #optimizer = optimizers.Adam(learning_rate=learning_rate)
    model.compile(loss='categorical_crossentropy', optimizer="adam" , metrics=['accuracy'])

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
        verbose=1
    )

    print(f"✅ Model trained on {len(X_train)} rows with min val accuracy: {round(np.min(history.history['accuracy']), 2)}")

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
    # predict on a sample text without padding.
    #sample_text = ('The movie was not good. The animation and the graphics '
    #           'were terrible. I would not recommend this movie.')
    predictions = model.predict(X_new)
    print(predictions)
