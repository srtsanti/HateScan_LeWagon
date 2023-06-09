import pandas as pd


def clean_data():
    df = pd.read_csv('/Users/Corcho/code/srtsanti/HateScan/HateScan/data/twitter_data1000.csv')
    
    df['TweetText'].fillna('', inplace=True)
    
    return df