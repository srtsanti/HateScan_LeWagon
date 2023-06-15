import streamlit as st
import pandas as pd
import numpy as np
import time
import bigquery
import requests

# Google imports
from google.oauth2 import service_account
from google.cloud import bigquery


#  GET data from BigQuery
# Create API client.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
client = bigquery.Client(credentials=credentials)

def run_query(query):
    query_job = client.query(query)
    rows_raw = query_job.result()
    # Convert to list of dicts. Required for st.cache_data to hash the return value.
    rows = [dict(row) for row in rows_raw]
    df = pd.DataFrame(rows)
    return df

def transform_hate_label(scale):
            if 0 <= scale < 0.85:
                return 0
            elif 0.85 <= scale < 1.5:
                return 1
            elif scale >= 1.5:
                return 2

def format_hate_scale(value):
    if value == 0:
        return "🙂"
    elif value == 1:
        return "😡"
    elif value == 2:
        return "🤬"
    else:
        return str(value)

def single_scan_page():

    spacing = '''
        <style>
            .spacing {
                margin-top: 200px;
            }
        </style>
    '''
    gap = '''
        <style>
            .gap {
                margin-top: 50px;
            }
        </style>
    '''
    my_slider = '''
        <style>
            .st-e1 {
                height: 20px;
            }
            .css-1vzeuhh {
                height: 1.5rem;
                width: 1.5rem;
            }
        </stlye>
    '''

    # Emojis on our Hate Scale
    scale_mapping = {
            0: ("Normal", "🙂"),
            1: ("Offensive", "😡"),
            2: ("Hate", "🤬")
        }

    # Hate Scan Title
    st.title('HateScan :mega: ')
    st.write('Welcome to our Hate Speech recognition app')

    # Gap CSS
    st.markdown(spacing, unsafe_allow_html=True)
    st.markdown('<div class="gap"></div>', unsafe_allow_html=True)

    # Tweet Box
    st.subheader('Enter tweet to analyze:')
    tweet = st.text_area("Tweet Box", max_chars=300)

    # API conn
    url = st.secrets['key_ap']
    params = {'tweet' : tweet}
    st.write(tweet)
    scanner = st.button('Scan tweet')

    # Gap CSS
    st.markdown(my_slider, unsafe_allow_html=True)

    # Initialize topics as an empty dictionary
    topics = {}

    # This is the code for printing the Hate scale
    if scanner:
        response = requests.get(url, params=params)
        #Connection to model_scale through our API
        scale = response.json()['hate_scale']['HateLabel']
        scale = transform_hate_label(scale)
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

        st.markdown(spacing, unsafe_allow_html=True)
        st.markdown('<div class="gap"></div>', unsafe_allow_html=True)

        # Sub-section 3: Hate Topic Prediction
        st.subheader("Hate Topic Prediction:")

        # Sort the topics dictionary by value in descending order
        sorted_topics = sorted(topics.items(), key=lambda x: x[1], reverse=True)

        # Get the class name with the largest value
        class_name_max = ""
        value_max = 0
        for key, value in sorted_topics:
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

            if value > value_max:
                value_max = value
                class_name_max = class_name

            if class_name == class_name_max:
                st.markdown(f"<span style='font-size: 1.2em; color: red;'>{class_name}: {round((value*100))}%</span>", unsafe_allow_html=True)
            else:
                st.write(f"{class_name}: {round((value*100))}%")
