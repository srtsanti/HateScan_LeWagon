import streamlit as st
import time
import requests

st.title('Welcome to the Hater Scan App')

url = st.secrets['key_ap']

st.title("Tweet Box")
tweet = st.text_area("Enter your tweet:", max_chars=200)
params = {'tweet' : tweet}
st.write("Your tweet:")
st.write(tweet)
scanner = st.button('Scan tweet')

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

if scanner:
    response = requests.get(url, params=params)
    #st.write(response.json())
    scale = response.json()['hate_scale']['HateLabel']
    topics = response.json()['hate_class']
    if scale in scale_mapping:
        label, emoji = scale_mapping[scale]
        st.write("Hate Label Scale:", f"{label} {emoji}")
        st.write("Hate Level:")
        
        st.select_slider("Your tweet is:",
                                  options=[0, 1, 2],
                                  value=scale,
                                  format_func=format_hate_scale)
    else:
        st.write("Hate Label Scale:", scale)
    
    st.write("                           ")
    st.write('Hate topics:')
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
