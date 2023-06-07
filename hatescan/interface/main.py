import numpy as np
import pandas as pd
from hatescan.ml_logic.data import clean_data
from hatescan.ml_logic.preprocessor import preprocessing, embedding, tokenizer, vectorizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical
from hatescan.ml_logic.model import initialize_model, compile_model, train_model
from hatescan.ml_logic.registry import save_model, load_model



#note: baseline model
baseline_model = 23/26

# def preprocess():
#     #clean dataset
#     df = clean_data()
#     df['Cleaned_text'] = df['TweetText'].apply(preprocessing)

#     #train X
#     X_train = tokenizer(df)

#     #vectorize words in sentence
#     word2vec = vectorizer(X_train)

#     # Embed the training and test sentences
#     X_train_embed = embedding(word2vec, X_train)

#     # Pad the training and test embedded sentences
#     X_train_pad = pad_sequences(X_train_embed, dtype='float32', padding='post', maxlen=200)

#     #define y
#     y = df[['HateLabel']]
#     y_cat = to_categorical(y)
    
#     return X_train_pad, y_cat
    
# def train():

#     #initiate model
#     model = initialize_model()

#     #compile model
#     model = compile_model(model=model, learning_rate=0.01)

#     #train model
#     model, history = train_model(model=model,
#             X_train=X_train_pad,
#             y_train=y_cat,
#             batch_size=32,
#             patience=2,
#             validation_split=0.2)
    
#     accuracy = np.min(history.history['val_accuracy'])

#     save_model(model=model)
    
#     return accuracy

#def pred(X_pred):
    # model = load_model()
    
    # #WE run the preprocessor for the x_new to get it preproceed to get prediction
    # X_processed = preprocessing(X_pred)
    
    # y_pred = model.predict(X_processed)
    # return y_pred
    
        
    
if __name__ == '__main__':
    preprocess()
    train()
    evaluate()
    pred()
    