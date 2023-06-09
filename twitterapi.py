import pandas as pd
import requests
from params import *
import time

df = pd.read_csv('data/hate_speech_dataset_v2.csv')
df = df[df['LangID'] == 1]

def get_text(id_number):

    url = "https://twitter135.p.rapidapi.com/v2/TweetDetail/"

    querystring = {"id":id_number}

    headers = {
    "X-RapidAPI-Key": "17f84b3e3dmsh705aa22617dea22p11e224jsn75fcf7665909",
    "X-RapidAPI-Host": "twitter135.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    return response.json()['data']['threaded_conversation_with_injections_v2']['instructions'][0]['entries'][0]['content']['itemContent']['tweet_results']['result']['legacy']['full_text']

for index, row in df.head(5).iterrows():
    time.sleep(0.255)  # to avoid hitting rate limits
    tweet_id = row['TweetID']
    try:
        tweet_text = get_text(tweet_id)
        row['TweetText'] = tweet_text
    except Exception as e:
        print(f"Failed to fetch tweet with id {tweet_id}. Error: {e}")
        row['TweetText'] = 'N/A'  # or whatever you want to denote a failed fetch
    # append each row to csv file
    if index == 23891: #FIRST ENGLISH TWEET
        row.to_frame().transpose().to_csv("twitter_data.csv", mode='w',header=True, index=False)
    else:
        row.to_frame().transpose().to_csv("twitter_data.csv", mode='a',header=False, index=False)
