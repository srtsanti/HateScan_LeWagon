import streamlit as st
import pandas as pd
from google.oauth2 import service_account
from google.cloud import bigquery
from PIL import Image


# Set the background color and font style
st.markdown(
    """
    <style>
    body {
        color: #333333;
        font-family: Arial, sans-serif;
        background-color: #F5F5F5;
    }
    .container {
        max-width: 800px;
        padding: 20px;
    }
    .title {
        font-size: 36px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 40px;
    }
    .subtitle {
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .text {
        font-size: 18px;
        margin-bottom: 20px;
    }
    .logo-image {
        display: block;
        margin: 0 auto;
        width: 300px;
        padding: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Display the layout
st.image('hatescan/app/logo_hscan.png', use_column_width=True)
st.markdown("<h1 class='title'>Hi, welcome to HateScan!</h1>", unsafe_allow_html=True)
st.markdown("<h2 class='subtitle'>Uncover linguistic patterns and gain insights from tweets</h2>", unsafe_allow_html=True)
st.markdown("<p class='text'>With HateScan, you can analyze language usage and preferred topics in tweets from friends, celebrities, and public figures. Compare individuals to gain a deeper understanding of speech patterns and explore prevalent topics.</p>", unsafe_allow_html=True)
st.markdown("<p class='text'>Uncover language nuances, identify recurring themes, and broaden your perspective on current events. HateScan empowers you to explore the power of language and gain valuable insights into those around you.</p>", unsafe_allow_html=True)
st.markdown("<p class='text'>Click on the nav icon on your left to start scanning!</p>", unsafe_allow_html=True)
