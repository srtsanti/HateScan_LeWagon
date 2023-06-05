import pandas as pd


def clean_data():
    df = pd.read_csv('../../data/df_sample25.csv')
    new_row = pd.DataFrame({
    'TweetID': [1344796664837637121],
    'LangID': [1],
    'TopicID': [1],
    'HateLabel': [2],
    'TweetText': ['I hate all people in this word!, I am really angry kill kill kill, death!']
    })
    df = pd.concat([df, new_row], ignore_index=True)
    df['TweetText'].fillna('', inplace=True)
    
    return df