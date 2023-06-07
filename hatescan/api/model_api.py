import numpy as np
import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from hatescan.ml_logic.registry import load_model
from hatescan.ml_logic.preprocessor import preprocessing, X_tokenizer, load_tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import text_to_word_sequence


app = FastAPI()
app.state.model = load_model()
app.state.tokenizer = load_tokenizer()

# Allowing all middleware is optional, but good practice for dev purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def root():
    return {
    'Welcome': 'Welcome to the API of HateScan!!'}
    

@app.get("/predict")
def predict(
        tweet: str,  # tweet string
    ):

    data = {'TweetText': str(tweet)}
    df = pd.DataFrame(data, index=[0])
    df['Cleaned_text'] = df['TweetText'].apply(preprocessing)

    X_new = [text_to_word_sequence(_) for _ in df["Cleaned_text"]]

    #Tokenize X
    loaded_tokenizer = load_tokenizer()
    X_pred_token= loaded_tokenizer.texts_to_sequences(X_new)

    #Pad X
    X_pred_pad = pad_sequences(X_pred_token, dtype='float32', padding='post')
    #Traer modelo
    model = app.state.model
    #pred modelo
    y_pred = model.predict(X_pred_pad)
    
    prediction = {'HateLabel': int(np.argmax(y_pred))}
    
    return prediction
