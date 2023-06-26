import numpy as np
import pandas as pd
from hatescan.ml_logic.data import load_clean_scaledata, load_clean_topicdata
from hatescan.ml_logic.preprocessor import preprocessing, tokenizer , load_tokenizer_scale_model, load_tokenizer_topic_model
from hatescan.ml_logic.models import initialize_model_scale, train_model_scale, evaluate_model_scale, initialize_model_topic, train_model_topic, evaluate_model_topic
from hatescan.ml_logic.registry import save_model_scale, save_model_topic, load_model_hatescale, load_model_hatetopic
from tensorflow.keras.preprocessing.text import text_to_word_sequence
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
        
def main_func_scale():
        #get + preproc dataset
        df = load_clean_scaledata()
        df['Cleaned_text'] = df['TweetText'].apply(preprocessing)
        X = [text_to_word_sequence(_) for _ in df["Cleaned_text"]]
        y = df[['HateLabel']]
        y_cat = to_categorical(y)
        X_train, X_test, y_train, y_test = train_test_split(X, y_cat, test_size=0.2, random_state=42)
        X_train_token, vocab_size = tokenizer(X_train)
        loaded_tokenizer = load_tokenizer_scale_model()
        X_test_token = loaded_tokenizer.texts_to_sequences(X_test)
        #Pad X
        X_train_pad = pad_sequences(X_train_token, dtype='float32', padding='post')
        X_test_pad = pad_sequences(X_test_token, dtype='float32', padding='post')
        
        #define params
        embedding_dimension = 100

        #initiate + compile model
        model = initialize_model_scale(vocab_size, embedding_dimension)

        #train model
        history, model = train_model_scale(
                model=model,
                X_train=X_train_pad,
                y_train=y_train,
                batch_size=32,
                patience=5,
                validation_split=0.2)
        
        test_loss, test_precision, test_acc = evaluate_model_scale(
        model=model,
        X=X_test_pad,
        y=y_test,
        batch_size=64)
        
        save_model_scale(model=model)

def main_func_topic():
        #get + preproc dataset
        df = load_clean_topicdata()
        df['Cleaned_text'] = df['TweetText'].apply(preprocessing)
        X = [text_to_word_sequence(_) for _ in df["Cleaned_text"]]
        y = df[['HateLabel']]
        y_cat = to_categorical(y)
        X_train, X_test, y_train, y_test = train_test_split(X, y_cat, test_size=0.2, random_state=42)
        X_train_token, vocab_size = tokenizer(X_train)
        loaded_tokenizer = load_tokenizer_topic_model()
        X_test_token = loaded_tokenizer.texts_to_sequences(X_test)
        #Pad X
        X_train_pad = pad_sequences(X_train_token, dtype='float32', padding='post')
        X_test_pad = pad_sequences(X_test_token, dtype='float32', padding='post')
        
        #define params
        embedding_dimension = 100

        #initiate + compile model
        model = initialize_model_topic(vocab_size, embedding_dimension)

        #train model
        history, model = train_model_topic(
                model=model,
                X_train=X_train_pad,
                y_train=y_train,
                batch_size=32,
                patience=5,
                validation_split=0.2)
        
        test_loss, test_acc = evaluate_model_topic(
        model=model,
        X=X_test_pad,
        y=y_test,
        batch_size=64)
        
        save_model_topic(model=model)

if __name__ == '__main__':
        main_func_scale()
        main_func_topic
