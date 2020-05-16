"""
Words2Graph 
Simple app to Visualize relationships in Texual data.

Author : Sreejith C
Find me @ https://sites.google.com/site/sreejithc321/

"""
from nltk import pos_tag
import networkx as nx
import matplotlib.pyplot as plt
from nltk.tokenize import word_tokenize
import streamlit as st
import re


def get_sov(text):
    """extract subject, action , object"""
    tokens = word_tokenize(text)
    tags = pos_tag(tokens)

    subject = action = object_ = False
    sub = act = obj = None

    for (word, pos) in tags:

        if pos.startswith('N') and subject == False:
            sub = word
            subject = True

        if pos in['VBG', 'VBD'] and action == False:
            act = word
            action = True

        if pos.startswith('N') and object_ == False and sub != word and action == True:
            obj = word
            object_ = True

    print(text, sub, act, obj)

    if sub and act and obj is not None:
        return (sub, act, obj)

    return None


def clean_document(text):
    """Remove non characters. Extra whitespace and stop words"""
    text = re.sub('[^A-Za-z .-]+', ' ', text)
    text = re.sub("[\[].*?[\]]", "", text)
    text = ' '.join(text.split())
    return text

st.title("Words2Graph ")
st.subheader(
    'An application to visualize [subject] <action> [object] relationships from texual data.')
#text = "Rahul plays cricket. Rahul lives in Mumbai. Mumbai is situated in Maharashtra. Shivaji ruled Maharashtra. Rahul likes Shivaji. "
text = "John is sleeping in a bed. Ted is reading a book. Kim is cooking in a pot. Ted is working with John. Kim is staying with John. Ted loves jogging with John. Bill is eating a steak. Joe likes walking with Ted. Kim is cooking a steak.Joe is drinking a beer. Henry is working with Joe."
text = st.text_area("Enter Your Text : ", text, key='text_analyzer')

if st.button('Visualize Data'):
    text = clean_document(text)
    sent = text.split('.')

    sov = []
    for item in sent:
        sov.append(get_sov(item))
    sov = list(filter(None.__ne__, sov))

    edge_labels = {}
    edges = []
    for item in sov:
        nodes = (item[0], item[2])
        edge_labels[nodes] = item[1]
        edges.append([item[0], item[2]])

    G = nx.Graph()
    G.add_edges_from(edges)
    pos = nx.spring_layout(G)

    nx.draw(G, pos, edge_color='black', width=1, linewidths=1,
            node_size=500, node_color='pink', alpha=0.9,
            labels={node: node for node in G.nodes()})

    nx.draw_networkx_edge_labels(
        G, pos, edge_labels=edge_labels, font_color='red')

    plt.axis('off')
    plt.savefig("Graph.png", format="PNG")
    st.image('Graph.png')
