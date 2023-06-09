import streamlit as st
import time

st.title('Welcome to the Hater Scan App')

st.title("Tweet Box")
tweet = st.text_area("Enter your tweet:", max_chars=200)
st.write("Your tweet:")
st.write(tweet)
scanner = st.button('Scan tweet')

def format_hate_scale(value):
    if value == 0:
        return "Normal"
    elif value == 1:
        return "Offensive"
    elif value == 2:
        return "Hate"
    else:
        return str(value)

st.title("Hate Scale")
hate_scale = st.select_slider("Your tweet is:",
                                  options=[0, 1, 2],
                                  value=0,
                                  format_func=format_hate_scale)

st.write("Your hate scale is :", format_hate_scale(hate_scale))
