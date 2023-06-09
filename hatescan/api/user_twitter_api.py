import requests

#with name_of_twitter_account input, get profile card    
def analyse_twitter_profile(input):    
    url = "https://twitter135.p.rapidapi.com/v2/UserByScreenName/"
    querystring = {"username":input}
    headers = {
	"X-RapidAPI-Key": "5b75ec0af7msh1bf64a6cc433349p125d64jsn5a59c3ca5bda",
	"X-RapidAPI-Host": "twitter135.p.rapidapi.com"
}
    response = requests.get(url, headers=headers, params=querystring).json()

    #get user's tweets
    rest_id = response['data']['user']['result']['rest_id']
    url = "https://twitter135.p.rapidapi.com/v2/UserTweets/"
    querystring = {"id":rest_id,
                "count":"40"}
    headers = {
        "X-RapidAPI-Key": "5b75ec0af7msh1bf64a6cc433349p125d64jsn5a59c3ca5bda",
        "X-RapidAPI-Host": "twitter135.p.rapidapi.com"
    }
    response_tweets = requests.get(url, headers=headers, params=querystring).json()

    #get list of 10 first tweets
    tweet_list=[]
    for i in range(0,10):
        tweet_list.append(response_tweets['data']['user']['result']['timeline_v2']['timeline']['instructions'][1]['entries'][i]['content']['itemContent']['tweet_results']['result']['legacy']['full_text'])
        
    return tweet_list    
        