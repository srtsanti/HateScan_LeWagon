import pandas as pd
import string
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.preprocessing.text import text_to_word_sequence
from gensim.models import Word2Vec
from tensorflow.keras.preprocessing.text import Tokenizer
import numpy as np
import nltk
import glob
import pickle
import unicodedata
import re

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')
nltk.download('wordnet')


def preprocessing(sentence):
    # Basic cleaning
    sentence = sentence.lower()
    sentence = sentence.strip() ## remove whitespaces
    sentence = sentence.replace('’', '')
    sentence = sentence.replace('"', '')
    sentence = sentence.replace('“', '')
    sentence = sentence.replace('”', '')
    sentence = sentence.replace('rt', '')

    sentence = sentence.lower() ## lowercase
    sentence = ''.join(char for char in sentence if not char.isdigit()) ## stay with letter
    sentence = ' '.join([word for word in sentence.split() if not word.startswith(('https', '@', '#', 'http'))]) #delete links, @mentions, #hashtags
    words = sentence.split()  # split into words
    words = [word for word in words if not any(substr in word for substr in ['https', '@', '#'])]  # delete words containing links, @, or #
    sentence = ' '.join(words)    # Remove emojis
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)
    sentence = emoji_pattern.sub(r'', sentence)

    # Advanced cleaning
    for punctuation in string.punctuation:
        sentence = sentence.replace(punctuation, '')## remove punctuation

    tokenized_sentence = word_tokenize(sentence) ## tokenize
    lemmatized = [WordNetLemmatizer().lemmatize(word, pos = "v") for word in tokenized_sentence]
    noun_lemmatized = [WordNetLemmatizer().lemmatize(word, pos = "n") for word in lemmatized]

    cleaned_text = ' '.join(word for word in noun_lemmatized)
    return cleaned_text

def tokenizer(X):
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(X)
    save_tokenizer(tokenizer)
    vocab_size = len(tokenizer.word_index)
    X_token = tokenizer.texts_to_sequences(X)
    return X_token, vocab_size

def save_tokenizer(tokenizer):
    # saving
    with open('token_pickle/tokenizer.pickle', 'wb') as handle:
        pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
def load_tokenizer_scale_model():
    # loading
    file_path = glob.glob('token_pickle_scale/*.pickle')[0]
    with open(file_path, 'rb') as handle:
        tokenizer = pickle.load(handle)
    return tokenizer
    
def load_tokenizer_topic_model():
    # loading
    file_path = glob.glob('token_pickle_topic/*.pickle')[0]
    with open(file_path, 'rb') as handle:
        tokenizer = pickle.load(handle)
    return tokenizer
