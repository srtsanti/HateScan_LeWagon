import streamlit as st
import numpy as np
import time
import pandas as pd
import plotly.graph_objects as go
import altair as alt


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
            .st-dv {
                height: 20px;
            }
            .css-1vzeuhh {
                height: 1.5rem;
                width: 1.5rem;
            }
        </stlye>
    '''

    # Hate Scan Title
    st.title('HateScan :mega: ')
    st.write('Welcome to our Hate Speech recognition app')

    # Gap CSS
    st.markdown(spacing, unsafe_allow_html=True)
    st.markdown('<div class="gap"></div>', unsafe_allow_html=True)

    # Tweet Box
    st.subheader('Enter tweet to analyze:')
    tweet = st.text_area("Tweet Box", max_chars=200)
    st.markdown("Scan:")
    st.write(tweet)
    scanner = st.button('Scan tweet')

    st.markdown(spacing, unsafe_allow_html=True)
    st.markdown('<div class="gap"></div>', unsafe_allow_html=True)

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

    # Section 2  - The Hate Scale
    st.subheader("Hate Scale")

    st.markdown(my_slider, unsafe_allow_html=True)
    hate_scale = st.select_slider("##### Hate level prediction:",
                                    options=[0, 1, 2],
                                    value=0,
                                    format_func=format_hate_scale
                                    )

    st.write("Your hate scale is :", format_hate_scale(hate_scale))

    st.markdown(spacing, unsafe_allow_html=True)
    st.markdown('<div class="gap"></div>', unsafe_allow_html=True)

    # Sub-section 3: Hate Topic Prediction
    st.subheader("Hate Topic Prediction")
    st.write('Prediction: Class 1 - Offensive 😡')
