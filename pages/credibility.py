import streamlit as st
import pandas as pd
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components
from similar_pdfs import *
from similar_topics import *
import nltk
import os
from datetime import datetime
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument


def word_count(text):
    return len(nltk.word_tokenize(text))

def extract_creation_date(pdf_path):
    try:
        with open(os.path.join("Dataset", "pdfs", pdf_path), 'rb') as file:
            parser = PDFParser(file)
            document = PDFDocument(parser)
            if 'CreationDate' in document.info[0]:
                creation_date = document.info[0]['CreationDate'].decode('utf-8')
                # D:20060915162758Z convert to YYYYmmdd 
                date_obj = datetime.strptime(creation_date[2:10], '%Y%m%d')
                formatted_date = date_obj.strftime('%Y%m%d')
                return formatted_date
            else:
                return None
    except Exception as e:
        print(f"Error extracting date from {pdf_path}: {e}")
        return None

def calculate_credibility(row, topics_freq):
    credibility = 0

    # Credibility based on topics
    topics = row['Topics']
    for topic in topics:
        if topic in topics_freq:
            freq = topics_freq[topic]
            credibility += freq * 0.4

    # Credibility based on word count
    word_count = row['WordCount']
    credibility += word_count * 0.01

    # Credibility based on recentness
    creation_date = row['CreationDate']

    if creation_date is not None:
        today = datetime.today()

        date_difference = (today - datetime.strptime(creation_date, '%Y%m%d')).days
        # the smaller the date difference, the larger the score
        credibility += (1/date_difference) * 100 

    return round(credibility, ndigits=2)

def extract_metrics(dataframe):
    topics_freq = dict()

    for topics in dataframe['Topics']:
        for topic in topics:
            if topic in topics_freq:
                topics_freq[topic] += 1
            else:
                topics_freq[topic] = 1

    dataframe['WordCount'] = dataframe['Text'].apply(word_count)

    dataframe['CreationDate'] = dataframe['PDF Path'].apply(extract_creation_date)

    dataframe['Credibility'] = dataframe.apply(lambda row: calculate_credibility(row, topics_freq), axis=1)
    for index, row in dataframe.iterrows():
        calculate_credibility(row, topics_freq)

    return dataframe

def filter_and_sort_df(df, input_topics):
    # Filter df to rows where the topics contain any of the input topics
    filtered_df = df[
        df['Topics'].apply(lambda topics: any(topic in topics for topic in input_topics)) 
    ]
    # Sort df by credibility
    filtered_df = filtered_df.sort_values(by='Credibility', ascending=False)
    
    if len(filtered_df) < 5:
        filtered_text_df = df[
        df['Text'].apply(lambda text: any(topic in text.lower() for topic in input_topics))
        ] 
        filtered_text_df = filtered_text_df.sort_values(by='Credibility', ascending=False)

        result = pd.concat([filtered_df, filtered_text_df])
        
        return result[['PDF Path', 'Credibility', 'Topics', 'CreationDate', 'Text']]
    else:
        return filtered_df[['PDF Path', 'Credibility', 'Topics', 'CreationDate', 'Text']] 


# Check if the DataFrame is in the session state
if 'filtered_df' in st.session_state:
    st.title("Your Filtered Dataframe")
    filtered_df = st.session_state['filtered_df']
    st.write(filtered_df)

    df_combined = pd.read_pickle("INTERMEDIATE_DF.pkl")  

    # Clean Text
    df_combined['Text'] = df_combined['Text'].apply(preprocess_text)
    
    df = extract_metrics(df_combined)

    ## User Interface
    st.title("Search the PDFs!")
    input_topics = st.text_input("Type in topics (comma-separated):")

    if input_topics:
        input_topics_list = [topic.strip().lower() for topic in input_topics.split(',')]
                
        sorted_df = filter_and_sort_df(df, input_topics_list)
        
        # show dataframe on streamlit
        st.write(sorted_df)


else:
    st.write("No data available. Please upload a CSV file on the main page.")



