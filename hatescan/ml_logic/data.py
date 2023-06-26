import pandas as pd


def load_clean_scaledata():
    df = pd.read_csv('data/prepped/concat_df.csv')

    return df

def load_clean_topicdata():
    df = pd.read_csv('data/prepped/twitter_davinci_ds.csv')

    return df