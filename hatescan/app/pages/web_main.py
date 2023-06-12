import streamlit as st

# Importing py files for the Navigation of HateScan App
import single_scan
import account_scan
import global_scan

PAGES = {
    "Single Scan": single_scan.single_scan_page,
    "Account Scan": account_scan.account_scan_page,
    "Global Scan": global_scan.global_scan_page
}

st.sidebar.title('Navigation')
page = st.sidebar.radio("Go to", list(PAGES.keys()))

PAGES[page]()
