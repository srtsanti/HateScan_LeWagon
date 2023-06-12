import streamlit as st
import web_app
import v2_web_app

PAGES = {
    # "Santi Web": web_app.show_web_app,
    "Joaqo Layout": v2_web_app.show_new_layout
}

st.sidebar.title('Navigation')
page = st.sidebar.radio("Go to", list(PAGES.keys()))

PAGES[page]()
