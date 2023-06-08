## IMPORTED MODEL FROM ROBERRTAAA
# Imported model from HuggingFace

import requests
from hatescan.params_hatescan import *

headers = {"Authorization": f"Bearer {API_TOKEN}"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()

def return_class(output):
  if 'LABEL_0' in output[0][0]['label']:
    if output[0][0]["score"] > 0.5:
      print("class 2: NEUTRAL")
      return "class 2: NEUTRAL"
    elif 0.3 <= output[0][0]["score"] <= 0.5:
      print("class 1: OFFENSIVE")
      return "class 1: OFFENSIVE"
    else:
      print("class 0: HATE")
      return "class 0: HATE"
  elif 'LABEL_1' in output[0][0]['label']:
    if output[0][0]["score"] > 0.7:
      print("class 2: HATE")
      return "class 2: HATE"
    elif 0.5 <= output[0][0]["score"] <= 0.3:
      print("class 1: OFFENSIVE")
      return "class 1: OFFENSIVE"
    else:
      print("class 0: NEUTRAL")
      return 'class 0: NEUTRAL'


def roberta_pred(input_tweet):
    output = query({"inputs": input_tweet})
    result = return_class(output)
    return result, output
