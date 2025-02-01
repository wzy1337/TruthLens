import streamlit as st
import pandas as pd
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components
from similar_pdfs import *
from similar_topics import *
from keybert import KeyBERT
import requests
from bs4 import BeautifulSoup

st.markdown('<style>div.block-container{padding-top:3rem;}</style>', unsafe_allow_html=True)

st.markdown(
    """
    Welcome to Truthlens, to proceed upload either a CSV file of pdfs or a CSV file of links
"""
)
# File uploader
uploaded_file_pdfs = st.file_uploader(":file_folder: Upload a CSV file for pdfs", type=["csv"], key="pdfs")
uploaded_file_news = st.file_uploader(":file_folder: Upload a CSV file for news", type=["csv"])

@st.cache_data(persist=True)
def load_data(file):
    return pd.read_csv(file, low_memory=False)

def process_dataframe(df, identifier_colname, summarized_text_colname):
    # Extract unique topics and store them in a new column
    kw_model = KeyBERT()
    all_topics = set()

    def extract_topics(text):
        if not text.strip():
            return []
        try:
            return [topic for topic, _ in kw_model.extract_keywords(docs=text, keyphrase_ngram_range=(1, 1), use_mmr=True, diversity=0.5)]
        except ValueError:
            return []

    if 'all_topics' not in st.session_state:
    # if 'Topics' not in df.columns:
        df['Topics'] = df[summarized_text_colname].apply(extract_topics)
        for topics in df['Topics']:
            all_topics.update(topics)
        st.session_state['all_topics'] = all_topics
    else:
        all_topics = st.session_state['all_topics']

    # Add a filter in the sidebar
    selected_topics = st.sidebar.multiselect("Filter by topics", list(all_topics))

    # Filter the DataFrame based on selected topics
    if selected_topics:
        filtered_df = df[df['Topics'].apply(lambda topics: all(topic in topics for topic in selected_topics))]
    else:
        filtered_df = df

    # Store the filtered DataFrame in the session state
    st.session_state['filtered_df'] = filtered_df



    if not filtered_df.empty:
        st.write(f"Number of documents matching the selected topics: {len(filtered_df)}")

        if len(filtered_df) == 1:
            st.write("Only one document matches the selected topics.")
            st.write(filtered_df.iloc[0])
        elif len(filtered_df) >=50:
            st.write("List of matching documents:")
            st.write("Only the first 50 documents are showed here")
            doc_list = ", ".join(filtered_df[identifier_colname].head(50).tolist())
            st.write(doc_list)
        else:
            st.write("List of matching documents:")
            doc_list = ", ".join(filtered_df[identifier_colname].tolist())
            st.write(doc_list)

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
                                                 identifier_colname=identifier_colname,
                                                 summarized_text_colname=summarized_text_colname)

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
        tab2.subheader("Similar Documents")

        with tab1:
            components.html(open('topics.html', 'r', encoding='utf-8').read(), width=800, height=600)
        with tab2:
            components.html(open('similarity.html', 'r', encoding='utf-8').read(), width=800, height=600)
    else:
        st.write("No documents match the selected topics.")

def fetch_webpage_text(url):
    """
    Fetch the text content from a webpage
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')
        text = ' '.join([para.get_text() for para in paragraphs])
        return text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return ""

# def preprocess_text(text):
#     """
#     Preprocess the text by removing unwanted characters, extra spaces, etc.
#     """
#     text = text.replace('\n', ' ')
#     text = text.replace('\r', ' ')
#     text = ' '.join(text.split())
#     return text

def extract_topics_from_urls(df, url_colname):
    """
    Extract topics from a DataFrame of URLs
    """
    kw_model = KeyBERT()
    # df['Text'] = df[url_colname].apply(fetch_webpage_text)
    df['Text'] = df['Text'].apply(preprocess_text)
    df['Topics'] = df['Text'].apply(lambda text: [topic for topic, _ in kw_model.extract_keywords(docs=text, keyphrase_ngram_range=(1, 1), use_mmr=True, diversity=0.5)])
    return df

# Check if the DataFrame is already in the session state
if 'df_combined' not in st.session_state:
    if uploaded_file_pdfs is not None:
        # Read the uploaded CSV file into a DataFrame
        df_combined = csv_to_dataframe(dataset_path=uploaded_file_pdfs, 
                                       identifier_colname='PDF Path',
                                       summarized_text_colname='Text'
                                       )
        st.session_state['df_combined'] = df_combined
    elif uploaded_file_news is not None:
        # Read the uploaded CSV file into a DataFrame
        df_combined = load_data(uploaded_file_news)
        df_combined = extract_topics_from_urls(df_combined, 'Link')
        st.session_state['df_combined'] = df_combined
else:
    df_combined = st.session_state['df_combined']

if 'df_combined' in st.session_state:
    df_combined = st.session_state['df_combined']

    if uploaded_file_pdfs is not None:
        process_dataframe(df_combined, identifier_colname='PDF Path', summarized_text_colname='Text')
    elif uploaded_file_news is not None:
        process_dataframe(df_combined, identifier_colname='Link', summarized_text_colname='Text')