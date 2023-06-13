import streamlit as st
import numpy as np
import time
import pandas as pd
import plotly.graph_objects as go
import altair as alt
import requests
from single_scan import *

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

    # This is the code for printing the Hate scale
    if scanner_user:
        response = requests.get(url_2, params=params_2)
        #Connection to model_scale through our API
        scale = response.json()['hate_scale']['HateLabel']
        #Connection to model_topic through our API
        topics = response.json()['hate_class']
        if scale in scale_mapping:
            label, emoji = scale_mapping[scale]
            st.write("Hate label prediction:", f"{label} {emoji}")
            st.subheader("Hate Scale:")

        else:
            st.write("Hate Label Scale:", scale)

    # This is the code for printing the Hate topics
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

    # Gap CSS
    st.markdown(gap, unsafe_allow_html=True)
    st.markdown('<div class="gap"></div>', unsafe_allow_html=True)

    # Account Metrics
    st.subheader('Account Metrics')

    # Assuming you have variables `num_tweets` and `hate_percentage` with the corresponding values

    # Create two columns
    col1, col2, col3 = st.columns(3)

    # Display the metrics in each column
    with col1:
        st.metric('Account Name', user)
    with col2:
        st.metric('Number of Tweets Analyzed', n_tweets)
    with col3:
        st.metric("Number of Hate Tweets", '3/15')

    # Create the DataFrame
    data = pd.DataFrame({
        'Category': ['Religion', 'Gender', 'Race', 'Politics', 'Sports'],
        'Number of Tweets': [2,4,5,6,1]
    })

    # Define the custom color palette by combining shades of red and purple
    color_palette = ['#FFD4D4', '#FFB2B2', '#FF9191', '#E6E6FA', '#D8C8F0']


    # Create the bar chart using Plotly
    fig = go.Figure(data=[go.Bar(x=data['Category'], y=data['Number of Tweets'], marker_color=color_palette)])

    # Add category labels
    fig.update_layout(
        annotations=[
            go.layout.Annotation(
                x=x,
                y=y,
                text=str(y),
                showarrow=False,
                font=dict(color='grey', size=16),
                xanchor='center',
                yanchor='bottom'
            ) for x, y in zip(data.index, data['Number of Tweets'])
        ],
        title="Number of Tweets by Category",
        title_font=dict(size=20, color="grey"),  # Specify non-bold font style using family parameter
        xaxis=dict(
            title="Category",
            title_font=dict(size=18),
            tickfont=dict(size=16)
        ),
        yaxis=dict(
            title="Number of Tweets",
            title_font=dict(size=18),
            tickfont=dict(size=16)
        )
    )

    # # Display the chart using Streamlit
    st.plotly_chart(fig)
