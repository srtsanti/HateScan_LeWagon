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

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')
nltk.download('wordnet')


def preprocessing(sentence):
    # Basic cleaning
    sentence = sentence.strip() ## remove whitespaces
    sentence = sentence.replace('’', '')
    sentence = sentence.lower() ## lowercase
    sentence = ''.join(char for char in sentence if char.isalpha() or char == " ") ## stay with letter
    ' '.join([ word for word in sentence.split() if not word.startswith('https') ]) #delete links

    # Advanced cleaning
    for punctuation in string.punctuation:
        sentence = sentence.replace(punctuation, '') ## remove punctuation

    tokenized_sentence = word_tokenize(sentence) ## split sentence into list
    stop_words = set(stopwords.words('english')) ## define stopwords

    tokenized_sentence_cleaned = [ w for w in tokenized_sentence if not w in stop_words] ## remove stopwords
    lemmatized = [WordNetLemmatizer().lemmatize(word, pos = "v") for word in tokenized_sentence_cleaned]
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
