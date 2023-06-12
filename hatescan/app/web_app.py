import streamlit as st
import time
import requests
from google.oauth2 import service_account
import pandas as pd
from google.cloud import bigquery
from hatescan.params_hatescan import *

st.title('Welcome to the Hater Scan App')

scale_mapping = {
        0: ("Normal", "🙂"),
        1: ("Offensive", "😡"),
        2: ("Hate", "🤬")
    }
def format_hate_scale(value):
    if value == 0:
        return "🙂"
    elif value == 1:
        return "😡"
    elif value == 2:
        return "🤬"
    else:
        return str(value)


#### THIS IS PAGE 1
url = st.secrets['key_ap']
st.title("Tweet Box")
tweet = st.text_area("Enter your tweet:", max_chars=300)
params = {'tweet' : tweet}
st.write("Your tweet:")
st.write(tweet)
scanner = st.button('Scan tweet')

# This is the code for printing the Hate scale
if scanner:
    response = requests.get(url, params=params)
    #Connection to model_scale through our API
    scale = response.json()['hate_scale']['HateLabel']
    #Connection to model_topic through our API
    topics = response.json()['hate_class']
    if scale in scale_mapping:
        label, emoji = scale_mapping[scale]
        st.write("Hate Label Scale:", f"{label} {emoji}")
        st.title("Hate Level:")
        st.select_slider("Your tweet is:",
                                  options=[0, 1, 2],
                                  value=scale,
                                  format_func=format_hate_scale)
    else:
        st.write("Hate Label Scale:", scale)
    
    st.markdown("---")
    
# This is the code for printing the Hate topics
    st.title('Hate topics:')
    for key, value in topics.items():
        class_name = ""
        if key == '0':
            class_name = "Religion"
        elif key == '1':
            class_name = "Gender"
        elif key == '2':
            class_name = "Race"
        elif key == '3':
            class_name = "Politics"
        elif key == '4':
            class_name = "Sports"
        st.write(f"{class_name}:  {value} %")


st.markdown("---")

#### THIS IS PAGE 2
url_2 = st.secrets['key_ap_user']

st.title("Twitter User profile")
user = st.text_area("Enter your user:", max_chars=50)
n_tweets = st.slider("Select a number between 5 and 50", 5, 50, 15)

params_2 = {'user' : user, 
            'n_tweets': n_tweets }

scanner_user = st.button('Scan user')

# This is the code for printing the Hate scale
if scanner_user:
    response = requests.get(url_2, params=params_2)
    #Connection to model_scale through our API
    scale = response.json()['hate_scale']['HateLabel']
    #Connection to model_topic through our API
    topics = response.json()['hate_class']
    if scale in scale_mapping:
        label, emoji = scale_mapping[scale]
        st.write("Hate Label Scale:", f"{label} {emoji}")
        st.title("Hate Level:")
        st.select_slider("Your tweet is:",
                                  options=[0, 1, 2],
                                  value=scale,
                                  format_func=format_hate_scale)
    else:
        st.write("Hate Label Scale:", scale)
    
    st.markdown("---")
    
# This is the code for printing the Hate topics
    st.title('Hate topics:')
    for key, value in topics.items():
        class_name = ""
        if key == '0':
            class_name = "Religion"
        elif key == '1':
            class_name = "Gender"
        elif key == '2':
            class_name = "Race"
        elif key == '3':
            class_name = "Politics"
        elif key == '4':
            class_name = "Sports"
        st.write(f"{class_name}:  {value} %")
    
# GET data from BigQuery
# Create API client.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
client = bigquery.Client(credentials=credentials)

# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def run_query(query):
    query_job = client.query(query)
    rows_raw = query_job.result()
    # Convert to list of dicts. Required for st.cache_data to hash the return value.
    rows = [dict(row) for row in rows_raw]
    return rows

# Load 10 rows
rows = run_query("SELECT * FROM 'crucial-strata-384013.UserName_HateScann' LIMIT 10")
# Show first 10 rows of DataFrame
df = pd.DataFrame(rows)
st.dataframe(df)
st.write(df)