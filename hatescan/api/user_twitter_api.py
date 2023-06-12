import pandas as pd
import requests
from hatescan.params_hatescan import *



#with name_of_twitter_account input, get profile card    
def analyse_twitter_profile(input, n_tweets_retreved):
    
    url = (TWITTER_USER_URL)
    querystring = {"username":input}
    headers = {
	"X-RapidAPI-Key":(X_RapidAPI_Key),
	"X-RapidAPI-Host":(X_RapidAPI_Host)
    }
    response = requests.get(url, headers=headers, params=querystring).json()
    user_name = response['data']['user']['result']['legacy']['screen_name']
    name_lastname = response['data']['user']['result']['legacy']['name']
    nr_followers = response['data']['user']['result']['legacy']['followers_count']
    is_verified = response['data']['user']['result']['legacy']['verified']
    media_count = response['data']['user']['result']['legacy']['media_count']

    #get user's tweets
    rest_id = response['data']['user']['result']['rest_id']
    url = (TWITTER_USERTWEET_URL)
    querystring = {"id":rest_id,
                "count":"40"}
    headers = {
        "X-RapidAPI-Key":(X_RapidAPI_Key),
        "X-RapidAPI-Host":(X_RapidAPI_Host)
    }
    response_tweets = requests.get(url, headers=headers, params=querystring).json()
    
    #get list of 10 first tweets
    tweet_list=[]
    try:
        for i in range(0,n_tweets_retreved):
            tweet_list.append(response_tweets['data']['user']['result']['timeline_v2']['timeline']['instructions'][1]['entries'][i]['content']['itemContent']['tweet_results']['result']['legacy']['full_text'])
    except:
        print("Twitter account does not have enough publications.")
    
    return tweet_list, user_name, name_lastname, nr_followers, is_verified, media_count