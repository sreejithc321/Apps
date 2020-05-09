"""
Review Analyser

Author : Sreejith C
Find me @ https://sites.google.com/site/sreejithc321/

"""
import streamlit as st
from bs4 import BeautifulSoup
from urllib.request import urlopen
from wordcloud import WordCloud, STOPWORDS
from gensim.summarization import summarize
import matplotlib.pyplot as plt 
from textblob import TextBlob
import spacy
import emoji
nlp = spacy.load('en_core_web_sm')


def web_scrap(url):
    try:
        page = urlopen(url) 
        soup = BeautifulSoup(page)
        # Fetch paragraphs
        data = ' '.join(map(lambda p:p.text,soup.find_all('p')))
        # Limit to 5000 character
        data = data [:5000]
        sent = data.split('.')
        # Remove non complete sentence from end
        clean_data = '. '.join(sent[:-1])
        data = clean_data +'.'
        if len(data) < 10 :
            return ('Unable to fetch data from the given URL !')
        else:
            return(data)
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
        return error

def main():

    data = ""
    html_temp = """
    <div style="background-color:black;padding:10px">
    <h1 style="color:white;text-align:center;">Review Analyser</h1>
    </div>
    """
    st.markdown(html_temp,unsafe_allow_html=True)
    st.text(" ")
    st.image('images.jpg',  width = 700)
    
    # Web Scrapping
    url = st.text_input("Enter Movie review URL : ")
    if st.button('Fetch Data'):
        data = web_scrap(url)
        st.info(data)

        # Word Cloud
        st.subheader("Word Cloud")
        wordcloud = WordCloud(background_color ='white', contour_width=3, 
                    contour_color='steelblue', stopwords = STOPWORDS).generate(data)
        plt.figure( figsize=(20,10), facecolor='k')
        plt.imshow(wordcloud,interpolation='bilinear')
        plt.axis("off")
        plt.tight_layout(pad=0)
        st.pyplot()

        # NER
        st.subheader("Celebrities / Characters / Entities ")
        result = get_ner(data)
        st.json(result)

        # Summary
        st.subheader("Summary of Review")
        result = summarize(data)
        st.info(result)

        # Sentiment
        st.subheader("Sentiment Analyser")
        blob = TextBlob(data)
        result = blob.sentiment.polarity
        if result > 0.6:
            custom_emoji = ':grinning_face_with_big_eyes:'
            st.write(emoji.emojize(custom_emoji,use_aliases=True))
        elif result > 0.3:
            custom_emoji = ':grinning_face:'
            st.write(emoji.emojize(custom_emoji,use_aliases=True))
        elif result > 0.0:
            custom_emoji = ':smile:'
            st.write(emoji.emojize(custom_emoji,use_aliases=True))
        elif result < 0.0:
            custom_emoji = ':disappointed:'
            st.write(emoji.emojize(custom_emoji,use_aliases=True))
        else:
            st.write(emoji.emojize(':expressionless:',use_aliases=True))
        st.info("Polarity Score is : {}".format(round(result,3)))


if __name__ =='__main__':
    main()