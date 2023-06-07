import numpy as np
import pandas as pd
from hatescan.ml_logic.data import clean_data
from hatescan.ml_logic.preprocessor import preprocessing, X_tokenizer, save_tokenizer, load_tokenizer
from hatescan.ml_logic.model import initialize_model, compile_model, train_model
from hatescan.ml_logic.registry import save_model, load_model
from tensorflow.keras.preprocessing.text import text_to_word_sequence
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical

from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

#baseline model
baseline_model = 23/26

def main_func():
        #get + preproc dataset
        df = clean_data()
        df['Cleaned_text'] = df['TweetText'].apply(preprocessing)

        X = [text_to_word_sequence(_) for _ in df["Cleaned_text"]]
        y = df[['HateLabel']]
        y_cat = to_categorical(y)
        X_train, X_test, y_train, y_test = train_test_split(X, y_cat, test_size=0.2, random_state=42)

        #Tokenize X
        X_train_token, vocab_size_train = X_tokenizer(X_train)

        loaded_tokenizer = load_tokenizer()
        X_test_token = loaded_tokenizer.texts_to_sequences(X_test)

        #Pad X
        X_train_pad = pad_sequences(X_train_token, dtype='float32', padding='post')
        X_test_pad = pad_sequences(X_test_token, dtype='float32',padding='post')


        #define params
        embedding_dimension = 100

        model = load_model()
        
        if model is None:
        #initiate model
                model = initialize_model(vocab_size_train, embedding_dimension)

        #     #compile model
        model = compile_model(model=model, learning_rate=0.01)

        #train model
        model, history = train_model(model=model,
                X_train=X_train_pad,
                y_train=y_train,
                batch_size=32,
                patience=2,
                validation_split=0.2)

        save_model(model=model)

# #predict y
# y_pred = model.predict(X_test_pad)
# y_pred_classes = np.argmax(y_pred, axis=1)
# y_test_classes = np.argmax(y_test, axis=1)

# #print classification report to check how often the most dangerous class was predict correctly
# report = classification_report(y_test_classes, y_pred_classes, target_names=['Class 0', 'Class 1', 'Class 2'])

if __name__ == '__main__':
        main_func()