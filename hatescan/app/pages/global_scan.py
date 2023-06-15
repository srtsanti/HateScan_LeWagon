import streamlit as st
import numpy as np
import time
import pandas as pd
import plotly.graph_objects as go
import altair as alt
import matplotlib.pyplot as plt
import seaborn as sns

def global_scan_page():

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

    # Hate Scan Title
    st.title('GlobalScan :mega:')
    st.write('Analysis of All Twitter Accounts Scanned by HateScan')

    # Gap CSS
    st.markdown(spacing, unsafe_allow_html=True)
    st.markdown('<div class="gap"></div>', unsafe_allow_html=True)

    # Assuming you have variables `num_tweets` and `hate_percentage` with the corresponding values
    accounts_num = 8
    num_tweets = 60
    hate_percentage = 90

    # Create three columns
    col1, col2 = st.columns(2)
    # Display the metrics in each column
    with col1:
        st.metric('Number of Accounts Analyzed', accounts_num)
    with col2:
        st.metric('Number of Tweets Analyzed', num_tweets)

    # Creating Tabs
    tab1, tab2, tab3 = st.tabs(["All", "Topic Distribution", "Mapping Predictions"])



    with tab1:
        # Create a DataFrame with the data for the stacked bar chart
        data = {
        'Hate Label': ['Normal', 'Offensive', 'Hate'],
        'Religion': [10, 20, 15],
        'Race': [5, 10, 7],
        'Gender': [15, 30, 10]
        }
        df = pd.DataFrame(data)

        # Reshape the data into a format suitable for stacking
        df_stacked = df.melt('Hate Label', var_name='Variable', value_name='Value')

        # Define the custom color palette
        custom_palette = alt.Scale(domain=['Religion', 'Race', 'Gender', 'Politics', 'Sport'], range = ['#FFD4D4', '#FFB2B2', '#FF9191', '#E6E6FA', '#D8C8F0'])

        # Create the stacked bar chart using Altair
        chart = alt.Chart(df_stacked).mark_bar().encode(
            x='sum(Value):Q',
            y='Hate Label:O',
            color=alt.Color('Variable:N', scale=custom_palette)
        ).properties(
            width=400,
            height=200
        )

        # Display the chart using Streamlit
        st.altair_chart(chart, use_container_width=True)

        # Generate random data within the desired range
        chart_data = pd.DataFrame(
            np.random.uniform(0, 10, size=(20, 3)),
            columns=['a', 'b', 'c'])

        custom_palette = alt.Scale(domain=[0, 10], range=['#E6E6FA', '#9370DB', '#4B0082'])

        c = alt.Chart(chart_data).mark_circle().encode(
            x='a', y='b', size='c', color=alt.Color('c', scale=custom_palette), tooltip=['a', 'b', 'c'])

        st.altair_chart(c, use_container_width=True)




    with tab2:
        # Create a DataFrame with the data for the stacked bar chart
        data = {
        'Hate Label': ['Normal', 'Offensive', 'Hate'],
        'Religion': [10, 20, 15],
        'Race': [5, 10, 7],
        'Gender': [15, 30, 10]
        }
        df = pd.DataFrame(data)

        # Reshape the data into a format suitable for stacking
        df_stacked = df.melt('Hate Label', var_name='Variable', value_name='Value')

        # Define the custom color palette
        custom_palette = alt.Scale(domain=['Religion', 'Race', 'Gender'], range=['#FFD4D4', '#FFA7A7', '#FF7B7B'])

        # Create the stacked bar chart using Altair
        chart = alt.Chart(df_stacked).mark_bar().encode(
            x='sum(Value):Q',
            y='Hate Label:O',
            color=alt.Color('Variable:N', scale=custom_palette)
        ).properties(
            width=400,
            height=200
        )

        # Display the chart using Streamlit
        st.altair_chart(chart, use_container_width=True)

    with tab3:
        # Generate random data within the desired range
        chart_data = pd.DataFrame(
            np.random.uniform(0, 10, size=(20, 3)),
            columns=['a', 'b', 'c'])

        custom_palette = alt.Scale(domain=[0, 10], range=['#E6E6FA', '#9370DB', '#4B0082'])

        c = alt.Chart(chart_data).mark_circle().encode(
            x='a', y='b', size='c', color=alt.Color('c', scale=custom_palette), tooltip=['a', 'b', 'c'])

        st.altair_chart(c, use_container_width=True)
