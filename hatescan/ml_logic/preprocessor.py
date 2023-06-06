import pandas as pd
import string
from nltk.corpus import stopwords 
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer

def preprocessing(sentence):
    # Basic cleaning
    sentence = sentence.strip() ## remove whitespaces
    sentence = sentence.lower() ## lowercase 
    sentence = ''.join(char for char in sentence if char.isalpha()) ## stay with letter
    # Advanced cleaning
    for punctuation in string.punctuation:
        sentence = sentence.replace(punctuation, '') ## remove punctuation
    
    tokenized_sentence = word_tokenize(sentence) ## tokenize 
    stop_words = set(stopwords.words('english')) ## define stopwords
    
    tokenized_sentence_cleaned = [ w for w in tokenized_sentence if not w in stop_words] ## remove stopwords
    lemmatized = [WordNetLemmatizer().lemmatize(word, pos = "v") for word in tokenized_sentence_cleaned]
    noun_lemmatized = [WordNetLemmatizer().lemmatize(word, pos = "n") for word in lemmatized]
    cleaned_text = ' '.join(word for word in noun_lemmatized)
    return cleaned_text


def vectorizer(df):
    vectorizer = TfidfVectorizer()
    vectorizer_text = vectorizer.fit_transform(df['Cleaned_text'])
    vectorizer_text = pd.DataFrame(
        vectorizer_text.toarray(), 
        columns = vectorizer.get_feature_names_out()
    )
