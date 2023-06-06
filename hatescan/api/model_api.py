import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from hatescan.ml_logic.registry import load_model
from hatescan.ml_logic.preprocessor import preprocessing, embedding, tokenizer, vectorizer
from tensorflow.keras.preprocessing.sequence import pad_sequences


app = FastAPI()
app.state.model = load_model()

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
    
    X_pred = pd.DataFrame(data, index=['TweetText'])
    
    X_pred['Cleaned_text'] = X_pred['TweetText'].apply(preprocessing)
    X_pred_token = tokenizer(X_pred)
    pred_word2vec = vectorizer(X_pred_token)
    X_pred_embed = embedding(pred_word2vec, X_pred_token)
    X_pred_pad = pad_sequences(X_pred_embed, dtype='float32', padding='post', maxlen=200)

    #Traer modelo
    model = app.state.model
    #pred modelo
    y_pred = model.predict(X_pred_pad)
    
    prediction = {'HateLabel': y_pred[0][0]}
    
    return prediction
