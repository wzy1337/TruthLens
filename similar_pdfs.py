import nltk
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet
import networkx as nx
import pandas as pd
import re
import string

stop_words = set(nltk.corpus.stopwords.words('english'))
punctuation = set(string.punctuation).union({'`', '-', '``', '–', '“', '’', '”', '•'})
lemma = WordNetLemmatizer()



def renormalize(probs):
    """
    From a list of probabilities, scale them accordingly
    """

    prob_factor = (5 / sum(probs))**0.1**0.2
    return [prob_factor * p for p in probs]

def extract_number(pdf_path):
    """
    Extract the PDF number to sort PDFs from name i.e 1 from 1.pdf
    """
    match = re.search(r'\d+', pdf_path)
    return int(match.group()) if match else float('inf')

def lower_tt(text):
    """
    Returns an uncapitalised version of a text if it is written in Title Case
    """
    words = text.split()
    return ' '.join(map(lambda word: word.lower() if word.istitle() else word, words))

def tag_position(nltk_tag):
    """
    Returns the type of word in one of the 4 categories
    for lemmatizer
    """
    # ensure wornet corpus loaded
    wordnet.ensure_loaded()

    tagging_d = {
        'J': wordnet.ADJ, 'V': wordnet.VERB, 'N': wordnet.NOUN, 'R': wordnet.ADV
    }
    return tagging_d.get(nltk_tag[0], None)

def preprocess_text(text, group_sentences=False, return_string=True):
    """
    Breaks up text into sentences, and if required, further does not group the sentences
    returns as a list containing tokens, no distinguishing between sentences
    """
    # tokens = nltk.tokenize.word_tokenize(text)
    sentences = nltk.sent_tokenize(text)
    tokenized_words = [nltk.word_tokenize(sentence) for sentence in sentences]

    final_token_sentences = []

    for tokenized_sentences in tokenized_words:
        ## Lemmatization first - tag the tokens with position ADj, verb etc.
        tagged_tokens = nltk.pos_tag(tokenized_sentences)

        normalised_token_sentences = []
        skip = False
        for j in range(0, len(tagged_tokens)-1):
            if skip:
                skip = False
                continue

            word, tag = tagged_tokens[j][0], tagged_tokens[j][1]
            next_word, next_tag = tagged_tokens[j+1][0], tagged_tokens[j+1][1]
            
            # check if tag:next_tag is of type NN:CD  
            if tag.startswith("NN") and next_tag == "CD":
                combined_word = word + " " + next_word
                normalised_token_sentences.append(combined_word)
                skip = True
            else:
                normalised_token_sentences.append(lemma.lemmatize(word))
                # if tag_position(tag):
                #     normalised_token_sentences.append(lemma.lemmatize(word, pos=tag_position(tag)))
                # else:
                #     normalised_token_sentences.append(lemma.lemmatize(word))

        ## Remove stopwords and punctuation
        cleaned_token_sentence = [lower_tt(word) for word in normalised_token_sentences if word.lower() not in stop_words and word not in punctuation and not word.isdigit()]
        final_token_sentences.append(cleaned_token_sentence)
    
    if group_sentences == False:
        if return_string == True:
            final_str = ''
            
            for sentence in final_token_sentences:
                for word in sentence:
                    final_str += " " + word
                final_str += ". "
            
            return final_str
        
        else:
            return [sentence for sentence in final_token_sentences]
    else:
        return final_token_sentences


def draw_similarity_graph(df_combined, identifier_colname, summarized_text_colname, threshold=0.3, output_file='similar.jpg'):
    """
    Inputs:
    - df_combined: dataset in dataframe form
    - identifier_colname: 
    
    """
    # Clean Text
    df_combined[summarized_text_colname] = df_combined[summarized_text_colname].apply(preprocess_text)
    
    # clean
    df_text = df_combined[summarized_text_colname]
    
    # Create a TF-IDF Vectorizer
    vectorizer = TfidfVectorizer(stop_words='english')

    # Fit and transform the text data
    tfidf_matrix = vectorizer.fit_transform(df_text)

    # Compute cosine similarity between all pairs of documents
    cosine_sim_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)
    G = nx.Graph()

    for i in range(len(df_text)):
        # G.add_node(df_combined[identifier_colname].iloc[i], title=df_combined[identifier_colname].iloc[i], group=1, size=10, shape='dot')

        for j in range(i + 1, len(df_text)):
            
            similarity = cosine_sim_matrix[i, j]

            if similarity > threshold:

                G.add_edge(
                    df_combined[identifier_colname].iloc[i], 
                    df_combined[identifier_colname].iloc[j], 
                    weight=similarity
                )

    # make similar connected groups same colour by assigning same groups
    grouped = list(nx.connected_components(G))
    for idx, group in enumerate(grouped):
        for doc in group:
            G.add_node(doc, title=doc, group=idx+1, size=10, shape='dot')

    return G
  
