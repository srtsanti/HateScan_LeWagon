import pandas as pd
import string
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.preprocessing.text import text_to_word_sequence
from gensim.models import Word2Vec
from tensorflow.keras.preprocessing.text import Tokenizer
import pickle
import numpy as np
import nltk

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

def X_tokenizer(X):
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
    
def load_tokenizer():
    # loading
    with open('token_pickle/tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)
    return tokenizer
    


# Function to convert a sentence (list of words) into a matrix representing the words in the embedding space
'''def embed_sentence(word2vec, sentence):
    embedded_sentence = []
    for word in sentence:
        if word in word2vec.wv:
            embedded_sentence.append(word2vec.wv[word])

    return np.array(embedded_sentence)'''

# Function that converts a list of sentences into a list of matrices
'''def embedding(word2vec, sentences):
    embed = []

    for sentence in sentences:
        embedded_sentence = embed_sentence(word2vec, sentence)
        embed.append(embedded_sentence)

    return embed'''
