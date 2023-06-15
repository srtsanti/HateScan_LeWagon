import streamlit as st
import pandas as pd
import numpy as np
import time

import plotly.graph_objects as go
import altair as alt
import requests

from hatescan.params_hatescan import *
from sklearn.decomposition import PCA
from google.oauth2 import service_account
from google.cloud import bigquery
import plotly.express as px

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

# Actual web page design
def account_scan_page():
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

    # Emojis on our Hate Scale
    scale_mapping = {
            0: ("Normal", "🙂"),
            1: ("Offensive", "😡"),
            2: ("Hate", "🤬")
        }

    def format_hate_scale(value):
        if value == 0:
            return "Normal 🙂"
        elif value == 1:
            return "Offensive 😡"
        elif value == 2:
            return "Hate 🤬"
        else:
            return str(value)

    # Hate Scan Title
    st.title('AccountScan :mega:')
    st.write('Welcome to our Hate Speech recognition app')

    # Gap CSS
    st.markdown(spacing, unsafe_allow_html=True)
    st.markdown('<div class="gap"></div>', unsafe_allow_html=True)

    ### API CON - Account Scan

    url_2 = st.secrets['key_ap_user']

    st.subheader("Enter Twitter username")
    user = st.text_input("Enter your user:", max_chars=50)

    n_tweets = st.slider("Select the number of tweets to analyze", 5, 50, 15)

    params_2 = {'user' : user,
                'n_tweets': n_tweets }

    scanner_user = st.button('Scan user')

    # Query to check if username is in BQ
    query_user_bq = f"""
    WITH temp_table as (
    SELECT *, LOWER(user_name) as name_lower FROM {GCP_PROJECT}.{BQ_DATASET}.{BQ_TABLE})
    SELECT * from temp_table
    WHERE name_lower = LOWER('{user}')
    """
    query_result = run_query(query_user_bq)

    if scanner_user:
        if not query_result.empty:
            hate_columns = ['hate_label','Religion_class', 'Gender_class', 'Race_class', 'Politics_class', 'Sports_class']
            hate_data = query_result[hate_columns]

            # This is the code for the Topics
            class_df = hate_data.drop('hate_label', axis=1)
            class_chart = class_df.melt()
            class_chart['variable'] = class_chart['variable'].str.replace('_class', '')

            scale = hate_data['hate_label'].item()
            scale = transform_hate_label(scale)


            # This is the code for printing the Hate topics
            st.subheader(f"Topic's {user} tweets about:")
            # Create two columns
            col1, col2, col3  = st.columns(3)

            # Display the metrics in each column
            with col1:
                st.metric('Account Name', user)
            with col2:
                st.metric('Number of Tweets Analyzed', n_tweets)
            with col3:
                if scale in scale_mapping:
                    label, emoji = scale_mapping[scale]
                    # st.write("Hate Label Scale:", f"{label} {emoji}")
                    st.metric("Number of Hate Tweets",f"{label} {emoji}")

            # Color palette of the graph
            color_palette = ['#D7667A', '#E8E29C', '#179A8E', '#7B3F61', '#3A6186']
            # Graph itself from DB
            db_fig_topics = px.bar(class_chart, x='variable', y='value', color='variable', title=f"Topic's {user} tweets about:", color_discrete_sequence=color_palette)
            st.plotly_chart(db_fig_topics, use_container_width=True)

        else:
            # This is the code for printing the Hate scale
            response = requests.get(url_2, params=params_2)
            #Connection to model_scale through our API
            scale = response.json()['hate_scale']['HateLabel']
            scale = transform_hate_label(scale)
            #Connection to model_topic through our API
            topics = response.json()['hate_class']

            # This is the code for printing the Hate topics
            st.subheader(f"Topic's {user} tweets about:")
            # Create two columns
            col1, col2, col3  = st.columns(3)

            with col1:
                st.metric('Account Name', user)
            with col2:
                st.metric('Number of Tweets Analyzed', n_tweets)
            with col3:
                if scale in scale_mapping:
                    label, emoji = scale_mapping[scale]
                    # st.write("Hate Label Scale:", f"{label} {emoji}")
                    st.metric("Number of Hate Tweets",f"{label} {emoji}")

            dfr = pd.DataFrame.from_dict(topics, orient='index', columns=['value'])
            dfr['variable'] = ['Religion', 'Gender', 'Race', 'Politics', 'Sports']
            api_fig_topics = px.bar(dfr, x='variable', y='value', color='variable', title=f"Topic's {user} tweets about:")
            st.plotly_chart(api_fig_topics, use_container_width=True)



    # Gap CSS
    st.markdown(gap, unsafe_allow_html=True)
    st.markdown('<div class="gap"></div>', unsafe_allow_html=True)
