import streamlit as st
import pandas as pd
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components
from similar_pdfs import *
from similar_topics import *

# File uploader
uploaded_file = st.file_uploader(":file_folder: Upload a CSV file", type=["csv"])
if uploaded_file is not None:

    # Read the uploaded CSV file into a DataFrame
    
    # Combine summarized text for those with a common identifier
    df_combined = csv_to_dataframe(dataset_path=uploaded_file, 
                                   identifier_colname='PDF Path',
                                   summarized_text_colname='Text'
                                   )


    topic_graph = draw_summary_graph(df_combined, threshold=0.2)

    # adjust node size based on their # of degrees
    topic_degrees = dict(topic_graph.degree)
    topic_degrees.update((x, 4*y) for x, y in topic_degrees.items())
    nx.set_node_attributes(topic_graph, topic_degrees, 'size')

    topic_nt = Network()
    topic_nt.from_nx(topic_graph)
    topic_nt.save_graph('topics.html')


    similarity_graph = draw_similarity_graph(df_combined,
                                            identifier_colname='PDF Path',
                                            summarized_text_colname='Text')

    # adjust node size based on their # of degrees
    sim_degrees = dict(similarity_graph.degree)
    sim_degrees.update((x, 4*y) for x, y in sim_degrees.items())
    nx.set_node_attributes(similarity_graph, sim_degrees, 'size')

    sim_nt = Network()
    sim_nt.from_nx(similarity_graph)
    sim_nt.save_graph('similarity.html')


    # Load HTML file in HTML component for display on Streamlit page
    tab1, tab2 = st.tabs(["Topics", "Similarity"])

    tab1.subheader("Common Topics")
    tab2.subheader("Similar PDFs")


    with tab1:
        components.html(open('topics.html', 'r', encoding='utf-8').read(), width=800, height=600)
    with tab2:
        components.html(open('similarity.html', 'r', encoding='utf-8').read(), width=800, height=600)
