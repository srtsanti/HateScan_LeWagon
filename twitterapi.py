import requests
from params import *

url = "https://twitter135.p.rapidapi.com/v2/TweetDetail/"

querystring = {"id":"{i}"}

headers = {
	"X-RapidAPI-Key": API_KEY,
	"X-RapidAPI-Host": "twitter135.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json()['data']['threaded_conversation_with_injections_v2']['instructions'][0]['entries'][0]['content']['itemContent']['tweet_results']['result']['legacy']['full_text'])
