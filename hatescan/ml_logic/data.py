import pandas as pd


def clean_data():
    df = pd.read_csv('../../data/df_sample25.csv')
    df['TweetText'].fillna('', inplace=True)
    
    return df