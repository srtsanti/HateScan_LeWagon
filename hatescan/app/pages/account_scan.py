import streamlit as st
import numpy as np
import time
import pandas as pd
import plotly.graph_objects as go
import altair as alt

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

    # Hate Scan Title
    st.title('AccountScan :mega:')
    st.write('Welcome to our Hate Speech recognition app')

    # Gap CSS
    st.markdown(spacing, unsafe_allow_html=True)
    st.markdown('<div class="gap"></div>', unsafe_allow_html=True)

    # Section 1 - Tweet Box
    st.subheader('Enter Twitter username:')
    tweet = st.text_area("Username Box", max_chars=50)
    st.markdown("Scan:")
    st.write(tweet)
    scanner = st.button('Scan Account')


    # Gap CSS
    st.markdown(gap, unsafe_allow_html=True)
    st.markdown('<div class="gap"></div>', unsafe_allow_html=True)

    # Account Metrics
    st.subheader('Account Metrics')

    # Assuming you have variables `num_tweets` and `hate_percentage` with the corresponding values
    num_tweets = 10
    hate_label_acc = 'Offensive'

    # Create two columns
    col1, col2, col3 = st.columns(3)

    # Display the metrics in each column
    with col1:
        st.metric('Account Name', 'Joaqo')
    with col2:
        st.metric('Number of Tweets Analyzed', num_tweets)
    with col3:
        st.metric("Hate Label of Account", 'Offensive')

    # Create the DataFrame
    data = pd.DataFrame({
        'Category': ['Religion', 'Gender', 'Race', 'Politics', 'Sport'],
        'Number of Tweets': [2, 5, 1, 2, 5]
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

    # Display the chart using Streamlit
    st.plotly_chart(fig)
