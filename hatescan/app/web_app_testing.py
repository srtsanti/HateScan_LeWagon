import streamlit as st
import time
import pandas as pd

# Hate Scan Title
st.title('Hate Scan :mega:')
st.markdown('#### Welcome to the Hate Scan App')


# Section 1 - Tweet Box
st.markdown("## Tweet Box")

tweet = st.text_area("#### Enter tweet:", max_chars=200)
st.markdown("Scan:")
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


# Section 2  - The Hate Scale
st.markdown("## Hate Scale")
hate_scale = st.select_slider("##### Hate label prediction:",
                                  options=[0, 1, 2],
                                  value=0,
                                  format_func=format_hate_scale)

st.write("Your hate scale is :", format_hate_scale(hate_scale))

# Here we have tabs to fuck around with
tab1, tab2 = st.tabs(["Tab 1", "Tab2"])

# Our data for the dataframe
data = {"a":[23, 12, 78, 4, 54], "b":[0, 13 ,88, 1, 3],
"c":[45, 2, 546, 67, 56]}


df = pd.DataFrame(data)
df
st.line_chart(data=df)
