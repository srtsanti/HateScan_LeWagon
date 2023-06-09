import numpy as np
import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from hatescan.ml_logic.registry import load_model_hatescale, load_model_hatetopic
from hatescan.ml_logic.preprocessor import preprocessing, X_tokenizer, load_tokenizer_scale_model, load_tokenizer_topic_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import text_to_word_sequence
from hatescan.api.user_twitter_api import analyse_twitter_profile


app = FastAPI()
app.state.model_1 = load_model_hatescale()
app.state.model_2 = load_model_hatetopic()
app.state.tokenizer_scale = load_tokenizer_scale_model()
app.state.tokenizer_topic = load_tokenizer_topic_model()

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
    'Welcome': 'Welcome to the API of HateScan 2!!'}
    

@app.get("/predict")
def predict(
        tweet: str,  # tweet string
    ):

    data = {'TweetText': str(tweet)}
    df = pd.DataFrame(data, index=[0])
    df['Cleaned_text'] = df['TweetText'].apply(preprocessing)
    
    X_new = [text_to_word_sequence(_) for _ in df["Cleaned_text"]]

    #Bring Tokenizer X
    loaded_tokenizer_scale = app.state.tokenizer_scale
    X_pred_token_scale= loaded_tokenizer_scale.texts_to_sequences(X_new)
    loaded_tokenizer_topic = app.state.tokenizer_topic
    X_pred_token_topic= loaded_tokenizer_topic.texts_to_sequences(X_new)
    
    #Pad X
    X_pred_pad_scale = pad_sequences(X_pred_token_scale, dtype='float32', padding='post')
    X_pred_pad_topic = pad_sequences(X_pred_token_topic, dtype='float32', padding='post')
        
    #Bring Modelos
    model_scale = app.state.model_1
    model_topic = app.state.model_2
    
    #Pred Model Scale
    y_pred_scale = model_scale.predict(X_pred_pad_scale)
    pred_scale = {'HateLabel': int(np.argmax(y_pred_scale))}

    #Pred Model Topic
    y_pred_topics = model_topic.predict(X_pred_pad_topic)
    list_topics = list(np.round(y_pred_topics[0], 3))
    list_topics = [round(float(each), 3) for each in list_topics]
    dict_topics = dict(zip(range(0,5),list_topics))
    
    return {'hate_scale' : pred_scale, 
            'hate_class': dict_topics}

@app.get("/predict_user")
def predict(
        user: str,  # tweet string
    ):

    #Getting the list of tweets from API Twitter
    list_of_tweets = analyse_twitter_profile(user)
    
    df = pd.DataFrame(list_of_tweets, columns='TweetText')
    
    df['Cleaned_text'] = df['TweetText'].apply(preprocessing)
    
    X_new = [text_to_word_sequence(_) for _ in df["Cleaned_text"]]

    #Bring Tokenizer X
    loaded_tokenizer_scale = app.state.tokenizer_scale
    X_pred_token_scale= loaded_tokenizer_scale.texts_to_sequences(X_new)
    loaded_tokenizer_topic = app.state.tokenizer_topic
    X_pred_token_topic= loaded_tokenizer_topic.texts_to_sequences(X_new)
    
    #Pad X
    X_pred_pad_scale = pad_sequences(X_pred_token_scale, dtype='float32', padding='post')
    X_pred_pad_topic = pad_sequences(X_pred_token_topic, dtype='float32', padding='post')
        
    #Bring Modelos
    model_scale = app.state.model_1
    model_topic = app.state.model_2
    
    #Pred Model Scale
    result_list = []
    for ele in X_pred_pad_scale:
        result_list.append(model_scale.predict(ele))
    # We need to see what to do as thershold 
    avg_ypred_scale = np.average(result_list)
    pred_scale = {'HateLabel': int(np.argmax(avg_ypred_scale))}
    
    #Pred Model Topic
    breakpoint()
    topic_results = []
    for ele in X_pred_pad_topic:
        topic_results.append(model_topic.predict(ele))
    
    
    
    list_topics = list(np.round(y_pred_topics[0], 3))
    list_topics = [round(float(each), 3) for each in list_topics]
    dict_topics = dict(zip(range(0,5),list_topics))
    
    return {'hate_scale' : pred_scale, 
            'hate_class': dict_topics}
