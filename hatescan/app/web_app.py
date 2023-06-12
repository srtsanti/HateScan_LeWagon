import streamlit as st
import time
import requests

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