import requests

url = "https://twitter135.p.rapidapi.com/v2/TweetDetail/"

querystring = {"id":"1344794359233998850"}

headers = {
	"X-RapidAPI-Key": "17f84b3e3dmsh705aa22617dea22p11e224jsn75fcf7665909",
	"X-RapidAPI-Host": "twitter135.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())
