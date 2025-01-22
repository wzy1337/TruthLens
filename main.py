import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(page_title="Superstore!!", page_icon=":bar_chart:", layout="wide")

# Title and styling
st.title(":bar_chart: Lenstruth")
st.markdown('<style>div.block-container{padding-top:3rem;}</style>', unsafe_allow_html=True)

# File uploader
fl = st.file_uploader(":file_folder: Upload a file", type=["csv", "xls"])