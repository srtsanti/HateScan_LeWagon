import numpy as np
import pandas as pd
from hatescan.ml_logic.data import clean_data
from hatescan.ml_logic.preprocessor import preprocessing, tokenizer
from hatescan.ml_logic.model import initialize_model, compile_model, train_model


from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical

from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

#baseline model
baseline_model = 23/26

#get + preproc dataset
df = clean_data()
df['Cleaned_text'] = df['TweetText'].apply(preprocessing)

X = [text_to_word_sequence(_) for _ in df["Cleaned_text"]]
y = df[['HateLabel']]
y_cat = to_categorical(y)
X_train, X_test, y_train, y_test = train_test_split(X, y_cat, test_size=0.2, random_state=42)

#Tokenize X
X_train_token, vocab_size = tokenizer(X_train)
X_test_token, _ = tokenizer(X_test)

#Pad X
X_train_pad = pad_sequences(X_train_token, dtype='float32', padding='post')
X_test_pad = pad_sequences(X_test_token, dtype='float32', padding='post')

#define params
embedding_dimension = 100

#initiate model
model = initialize_model(vocab_size, embedding_dimension)

#compile model
model = compile_model(model=model, learning_rate=0.01)

#train model
history, model = train_model(model=model,
        X_train=X_train_pad,
        y_train=y_train,
        batch_size=32,
        patience=2,
        validation_split=0.2)


#predict y
y_pred = model.predict(X_test_pad)
y_pred_classes = np.argmax(y_pred, axis=1)
y_test_classes = np.argmax(y_test, axis=1)

#print classification report to check how often the most dangerous class was predict correctly
report = classification_report(y_test_classes, y_pred_classes, target_names=['Class 0', 'Class 1', 'Class 2'])
