"""
TwitterStreamer

Author : Sreejith C
Find me @ https://sites.google.com/site/sreejithc321/
"""

import streamlit as st
from twitterscraper import query_tweets
from textblob import TextBlob
import datetime as dt
import spacy
import emoji
import re
nlp = spacy.load('en_core_web_sm')

def clean_data(data):
    try:
        data = str(data)
        data = data.replace('#',' ')
        data = data.replace('@', ' ')
        data = re.sub(r'@[A-Za-z0-9]+','',data)
        data = re.sub('https?://[A-Za-z0-9./]+','',data)
        data = re.sub("[^a-zA-Z]", " ", data)
        return data
    except Exception as error:
        return(error)

def get_ner(data):
    try:
        stop = ['email','copyright']
        docx = nlp(data)
        person = [ entity.text for entity in docx.ents if entity.label_ == 'PERSON']
        unique_person = []
        # Remove duplicates
        for x in person:
            if x.lower() in stop:
                continue
            if x not in unique_person:
                unique_person.append(x) 
        return unique_person
    except Exception as error:
        print(error)
        return []


st.header('TwitterStreamer')


query = st.text_input('Query:', '#')


if query != '' and query != '#':
    with st.spinner(f'Fetching tweets on {query}...'):

        tweets = query_tweets(query, begindate=dt.date.today() - dt.timedelta(weeks=1), lang='en')

        for tweet in tweets:
            text = TextBlob(tweet.text)
            st.warning(text)
            
            # Sentiment Analysis
            score = round(text.sentiment.polarity,3)
            if score > 0:
                sentiment = 'Positive'
                custom_emoji = ':grinning_face:'
            elif score < 0:
                sentiment  = 'Negative'
                custom_emoji = ':disappointed:'
            else:
                sentiment = 'Neutral'
                custom_emoji = ':expressionless:'
            result = 'Sentiment Analysis : ' + emoji.emojize(custom_emoji,use_aliases=True) + " -> " + sentiment +' : '+ str(score)
            st.info(result)
            
            # Keywords
            text = clean_data(text)
            result = get_ner(text)
            if len(result) > 0:
                entities = ", ".join(result)
                entities = 'Entities : ' + entities
                st.info(entities)