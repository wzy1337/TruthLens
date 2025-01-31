import streamlit as st
import pandas as pd
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components
from similar_pdfs import *
from similar_topics import *


# Check if the DataFrame is in the session state
if 'filtered_df' in st.session_state:
    filtered_df = st.session_state['filtered_df']
    st.write(filtered_df)
else:
    st.write("No data available. Please upload a CSV file on the main page.")

