import pandas as pd


def clean_data():
    df = pd.read_csv('../../data/twitter_data.csv')
    df['TweetText'].fillna('', inplace=True)
    
    return df