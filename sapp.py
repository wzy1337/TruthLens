import streamlit as st
import pandas as pd
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components
from similar_pdfs import *
from similar_topics import *

st.markdown('<style>div.block-container{padding-top:3rem;}</style>', unsafe_allow_html=True)

st.markdown(
    """
    Welcome to Truthlens, to proceed upload either a CSV file of pdfs or a CSV file of links
"""
)
# File uploader
uploaded_file_pdfs = st.file_uploader(":file_folder: Upload a CSV file for pdfs", type=["csv"], key="pdfs")
uploaded_file_news = st.file_uploader(":file_folder: Upload a CSV file for news", type=["csv"])

if uploaded_file_pdfs is not None:
    # Read the uploaded CSV file into a DataFrame
    df_combined = csv_to_dataframe(dataset_path=uploaded_file_pdfs, 
                                   identifier_colname='PDF Path',
                                   summarized_text_colname='Text'
                                   )

    # Extract unique topics
    kw_model = KeyBERT()
    all_topics = set()
    for text in df_combined['Text']:
        topics = kw_model.extract_keywords(docs=text, keyphrase_ngram_range=(1, 1), use_mmr=True, diversity=0.5)
        for topic, _ in topics:
            all_topics.add(topic)

    # Add a filter in the sidebar
    selected_topics = st.sidebar.multiselect("Filter by topics", list(all_topics))

    # Filter the DataFrame based on selected topics
    if selected_topics:
        filtered_df = df_combined[df_combined['Text'].apply(lambda x: any(topic in x for topic in selected_topics))]
    else:
        filtered_df = df_combined

    st.sidebar.header("Choose your filter: ")

    topic_graph = draw_summary_graph(filtered_df, threshold=0.2)

    # Adjust node size based on their number of degrees
    topic_degrees = dict(topic_graph.degree)
    topic_degrees.update((x, 4*y) for x, y in topic_degrees.items())
    nx.set_node_attributes(topic_graph, topic_degrees, 'size')

    topic_nt = Network()
    topic_nt.from_nx(topic_graph)
    topic_nt.save_graph('topics.html')

    # Generate similarity graph
    similarity_graph = draw_similarity_graph(filtered_df,
                                             identifier_colname='PDF Path',
                                             summarized_text_colname='Text')

    # Adjust node size based on their number of degrees
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