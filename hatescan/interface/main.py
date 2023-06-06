import numpy as np
import pandas as pd
from hatescan.ml_logic.data import clean_data
from hatescan.ml_logic.preprocessor import preprocessing, vectorizer


df = clean_data()

df['Cleaned_text'] = df['TweetText'].apply(preprocessing)
y = df[['HateLabel']]

df_vectorized = vectorizer(df)
df_vectorized['HateLabel'] = y

split_ratio: float = 0.2
# Create (X_train_processed, y_train, X_val_processed, y_val)
train_length = int(len(df_vectorized)*(1-split_ratio))

data_processed_train = df_vectorized.iloc[:train_length, :].sample(frac=1).to_numpy()
data_processed_val = df_vectorized.iloc[train_length:, :].sample(frac=1).to_numpy()

X_train_processed = data_processed_train[:, :-1]
y_train = data_processed_train[:, -1]

X_val_processed = data_processed_val[:, :-1]
y_val = data_processed_val[:, -1]
